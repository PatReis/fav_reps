import os
from django.conf import settings
from .models import Recipe, Topic


def clean_latex_escape_char(s):
    # Escape chars: & % $ # _ { } ~ ^ \
    s = s.replace("\\", "\\textbackslash")
    s = s.replace("~", "\\textasciitilde").replace("^", "\\textasciicircum")
    s = s.replace('&', '\\&').replace("%", "\\%").replace("$", "\\$").replace("#", "\\#").replace("_", "\\_")
    s = s.replace("{", "\\{").replace("}", "\\}")
    return s


def process_steps(steps):
    out = clean_latex_escape_char(steps)
    out = out.rstrip().replace('\r\n', '\n').split('\n')
    out = [x if x != '' else '\\\\' for x in out]
    out = " ".join(out)
    if out[-2:] == '\\\\':
        out = out[:-2]
    return out


def process_ingredients(ingred):
    out = clean_latex_escape_char(ingred)
    out = out.rstrip().replace('\r\n', '\n').replace('\n', ' | ')
    if out[-2:] != '\\\\':
        out += '\\\\'
    return out


def process_name(name):
    out = clean_latex_escape_char(name)
    out = out.rstrip()
    return out


def create_tex_file(file_path):
    recipes = Recipe.objects.all()
    with open(os.path.join(file_path, "book.tex"), 'w', encoding="utf-16") as f:
        with open(os.path.join(os.path.realpath(settings.STATICFILES_DIRS[0]), "latex", "header.tex"), 'r') as h:
            header = h.read()
            f.write(header)

        for i, recipe in enumerate(recipes):

            f.write(
                "\\subsection{%s}\n" % process_name(recipe.name)
            )
            f.write("\\textbf{Zutaten} für \\textit{%s} Personen: \\\\ \n" % recipe.persons)

            if recipe.ingredients:
                f.write(
                    process_ingredients(recipe.ingredients)
                )
                f.write("\n")

            f.write("\\\\ \\textbf{Zubereitung:} \\\\ \n")

            if recipe.steps:
                f.write(
                    process_steps(recipe.steps)
                )

            f.write("\n")

        with open(os.path.join(os.path.realpath(settings.STATICFILES_DIRS[0]), "latex", "footer.tex"), 'r') as h:
            footer = h.read()
            f.write(footer)

    return None
