import nox


@nox.session(python=["3.7", "3.8", "3.9", "3.10", "3.11"])
@nox.parametrize("willow", ["1.2", "1.3", "1.4"])
def tests(session, willow):
    session.install("-r", "requirements.txt")
    session.install("-r", "requirements.dev.txt")
    session.install(f"willow=={willow}")
    session.run("pytest")
