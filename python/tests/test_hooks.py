"""Tests for OpenAI patching and unpatching."""

import openai
import pytest

from aep_otel.hooks import patch_openai, unpatch_openai, _original_openai_chatcompletion_create, _patched_openai_chatcompletion_create


@pytest.fixture(autouse=True)
def ensure_unpatched_after_test():
    """Ensures that OpenAI is unpatched after each test in this module runs."""
    # This fixture runs before each test and then the yield allows the test to run.
    # After the test, the code below yield is executed.
    original_method_at_start = openai.resources.chat.completions.Completions.create
    try:
        yield
    finally:
        # Force unpatch if it was patched during a test, or restore if changed
        if openai.resources.chat.completions.Completions.create != _original_openai_chatcompletion_create and _original_openai_chatcompletion_create is not None:
            openai.resources.chat.completions.Completions.create = _original_openai_chatcompletion_create
        elif openai.resources.chat.completions.Completions.create != original_method_at_start:
             # If a test manually unpatched to something else or _original_openai_chatcompletion_create was None initially
             openai.resources.chat.completions.Completions.create = original_method_at_start

def test_openai_patch_unpatch():
    """Test that patch_openai and unpatch_openai correctly swap the method."""
    # Ensure we have the original method reference from the hooks module for comparison
    if _original_openai_chatcompletion_create is None:
        pytest.skip("Original OpenAI method not captured, cannot run patch test.")

    # Store the current create method
    original_method = openai.resources.chat.completions.Completions.create
    assert original_method == _original_openai_chatcompletion_create, "Test setup error: OpenAI already patched or original mismatch."

    # Patch OpenAI
    patch_openai()
    assert openai.resources.chat.completions.Completions.create == _patched_openai_chatcompletion_create, "Parching failed: Method not swapped to patched version."
    assert openai.resources.chat.completions.Completions.create != original_method, "Patching failed: Method is still the original."

    # Unpatch OpenAI
    unpatch_openai()
    assert openai.resources.chat.completions.Completions.create == original_method, "Unpatching failed: Method not restored to original."
    assert openai.resources.chat.completions.Completions.create == _original_openai_chatcompletion_create, "Unpatching failed: Method not restored to known original from hooks."

def test_idempotent_patch():
    """Test that patching multiple times doesn't break anything."""
    if _original_openai_chatcompletion_create is None:
        pytest.skip("Original OpenAI method not captured, cannot run patch test.")

    patch_openai()
    method_after_first_patch = openai.resources.chat.completions.Completions.create
    assert method_after_first_patch == _patched_openai_chatcompletion_create

    patch_openai() # Patch again
    assert openai.resources.chat.completions.Completions.create == _patched_openai_chatcompletion_create, "Patching a second time changed the method unexpectedly."

    unpatch_openai()
    assert openai.resources.chat.completions.Completions.create == _original_openai_chatcompletion_create

def test_idempotent_unpatch():
    """Test that unpatching multiple times doesn't break anything."""
    if _original_openai_chatcompletion_create is None:
        pytest.skip("Original OpenAI method not captured, cannot run patch test.")

    # Ensure it's patched first
    patch_openai()
    assert openai.resources.chat.completions.Completions.create == _patched_openai_chatcompletion_create

    unpatch_openai()
    method_after_first_unpatch = openai.resources.chat.completions.Completions.create
    assert method_after_first_unpatch == _original_openai_chatcompletion_create

    unpatch_openai() # Unpatch again
    assert openai.resources.chat.completions.Completions.create == _original_openai_chatcompletion_create, "Unpatching a second time changed the method unexpectedly." 