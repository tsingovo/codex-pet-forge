# Contributing

Run before submitting a change:

```powershell
python -m unittest discover -s tests -v
python C:\path\to\skill-creator\scripts\quick_validate.py plugins\codex-pet-forge\skills\pet-forge
python C:\path\to\plugin-creator\scripts\validate_plugin.py plugins\codex-pet-forge
```

Do not commit generated pets, user reference images, API keys, run folders, or application patches. Keep runtime-trigger assumptions isolated in `trigger-semantics.md` and update tests when Codex behavior changes.
