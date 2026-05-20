from pathlib import Path


def patch_student_labutils(root: Path) -> None:
    p = root / "scripts" / "labtainer-student" / "bin" / "labutils.py"
    text = p.read_text(encoding="utf-8")
    text = text.replace(
        """def getLastEmail():
    retval = None
    home_email = getHomeEmail()
    if os.path.isfile(home_email):
        with open(home_email) as fh:
            retval = fh.read()
            if retval is not None:
                retval = retval.strip()
    return retval

def putLastEmail(email):
    home_email = getHomeEmail()
    with open(home_email, 'w') as fh:
            fh.write(email)
""",
        """def getLastEmail():
    retval = None
    home_email = getHomeEmail()
    if os.path.isfile(home_email):
        with open(home_email) as fh:
            retval = fh.read()
            if retval is not None:
                retval = retval.strip().upper()
    return retval

def putLastEmail(email):
    home_email = getHomeEmail()
    with open(home_email, 'w') as fh:
            fh.write(email.strip().upper())
""",
    )
    text = text.replace(
        """            else:
                putLastEmail(user_email)
    return user_email
""",
        """            else:
                user_email = user_email.strip().upper()
                putLastEmail(user_email)
    return user_email
""",
    )
    p.write_text(text, encoding="utf-8")


def patch_instructor_gradelab(root: Path) -> None:
    p = root / "scripts" / "labtainer-instructor" / "bin" / "gradelab"
    text = p.read_text(encoding="utf-8")
    text = text.replace(
        "def CopyStudentArtifacts(labtainer_config, container_name, labname, regress_test, check_watermark):",
        "def CopyStudentArtifacts(labtainer_config, container_name, labname, regress_test, check_watermark, checkwork=False):",
    )
    text = text.replace(
        """    zip_filelist.extend(lab_filelist)
    #logger.debug("zip_filelist is (%s)" % zip_filelist)
""",
        """    if checkwork and regress_test is None:
        if len(lab_filelist) > 0:
            lab_filelist = [max(lab_filelist, key=os.path.getmtime)]
        zip_filelist = []
    zip_filelist.extend(lab_filelist)
    #logger.debug("zip_filelist is (%s)" % zip_filelist)
""",
    )
    text = text.replace(
        """    copy_result = CopyStudentArtifacts(labtainer_config, grade_container, labname, 
                     regress_test, False)""",
        """    copy_result = CopyStudentArtifacts(labtainer_config, grade_container, labname, 
                     regress_test, False, checkwork=checkwork)""",
    )
    p.write_text(text, encoding="utf-8")


def main() -> None:
    root = Path("/home/student/labtainer/trunk")
    patch_student_labutils(root)
    patch_instructor_gradelab(root)
    print("patched Labtainer core: uppercase student IDs and latest-only checkwork artifacts")


if __name__ == "__main__":
    main()
