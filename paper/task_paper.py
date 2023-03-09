"""Tasks for compiling the paper and presentation(s)."""
import shutil
import pytask
from pytask_latex import compilation_steps as cs
from final_project_productivity.config import BLD, PAPER_DIR

document = "final_project_productivity"

@pytask.mark.task(name="write_paper")
@pytask.mark.latex(
    script=PAPER_DIR / f"{document}.tex",
    document=BLD / "latex" / f"{document}.pdf",
    compilation_steps=cs.latexmk(
        options=("--pdf", "--interaction=nonstopmode", "--synctex=1", "--cd"),
    ),
)
def task_compile_document():
    """Compile the document specified in the latex decorator."""
    pass

kwargs = {
    "depends_on": BLD / "latex" / f"{document}.pdf",
    "produces": BLD.parent.resolve() / f"{document}.pdf",
}
@pytask.mark.task(id=document, kwargs=kwargs)
def task_copy_to_root(depends_on, produces):
    shutil.copy(depends_on, produces)