Labtainer core fix

This patch is for the Labtainer framework on the VM, not for the lab containers.

It fixes two issues:

1. Student ids/e-mail values entered at `labtainer -r <lab>` are normalized to uppercase.
2. `checkwork` only grades the newest `.lab` artifact for the current lab, so older saved attempts do not appear in the result table.

Apply on the Labtainer VM with:

```bash
python3 apply-labtainer-core-fix.py
```

The script updates:

- `/home/student/labtainer/trunk/scripts/labtainer-student/bin/labutils.py`
- `/home/student/labtainer/trunk/scripts/labtainer-instructor/bin/gradelab`

This fix is VM/framework-level, so rebuilding Docker images alone does not apply it.
