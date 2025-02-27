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


def translate_diff_to_text(d):
    if d < 0.5:
        return "\\textit{einfach}"
    if 0.5 <= d < 1.5:
        return "\\textit{mittel}"
    if 1.5 <= d < 2.5:
        return "\\textit{schwer}"
    if d >= 2.5:
        return "\\textit{profi}"
    return "-"


def create_tex_file(file_path, add_image=False):
    recipes = Recipe.objects.all().order_by('name')
    with open(os.path.join(file_path, "book.tex"), 'w', encoding="utf-16") as f:
        with open(os.path.join(os.path.realpath(settings.STATICFILES_DIRS[0]), "latex", "header.tex"), 'r') as h:
            header = h.read()
            f.write(header)

        for i, recipe in enumerate(recipes):

            f.write(
                "\\subsection{%s}\n" % process_name(recipe.name)
            )

            f.write(
                "Bewertung {0:.1f} ${4}$, Gesamtzeit: {1:.0f} min, Schwierigkeit: {2}, Karlorien: {3} kcal \\\\ \n".format(
                    recipe.rating, recipe.expected_time_total,
                    translate_diff_to_text(recipe.difficulty),
                    int(recipe.nutrients_person) if recipe.nutrients_person > 0 else "-",
                    "\\star"*int(recipe.rating) if 0 < recipe.rating < 6 else "-"
                )
            )

            image_has_been_added = False
            if add_image and recipe.image_meal is not None:
                if len(str(recipe.image_meal)) > 0:
                    f.write(
                        "\\begin{figure}[H] \n \\centering \n \\includegraphics[width=0.3\\textwidth]{%s} \n \\end{figure} \n " % recipe.image_meal
                    )
                    image_has_been_added = True

            if not image_has_been_added:
                f.write(" \\\\ ")

            f.write(
                "\\textbf{Zutaten} für \\textit{%s} Personen: \\\\ \n" % recipe.persons
            )

            if recipe.ingredients:
                f.write(
                    process_ingredients(recipe.ingredients)
                )
                f.write("\n")

            f.write(
                "\\\\ \\textbf{Zubereitung:} \\\\ \n"
            )

            if recipe.steps:
                f.write(
                    process_steps(recipe.steps)
                )

            if recipe.tips is not None:
                if len(recipe.tips) > 3:
                    if len(recipe.tips) > 2000:
                        f.write(
                            "\\\\ \\textit{Info:} Mehr Tipps online."
                        )
                    else:
                        f.write(
                            "\\\\ \\textit{Tipp:} "
                        )
                        if len(recipe.tips) > 1000:
                            f.write(
                                process_steps(recipe.tips[:1000])
                            )
                            f.write(" ($\\dots$) .")
                        else:
                            f.write(
                                process_steps(recipe.tips)
                            )

            f.write("\n")

        with open(os.path.join(os.path.realpath(settings.STATICFILES_DIRS[0]), "latex", "footer.tex"), 'r') as h:
            footer = h.read()
            f.write(footer)

    return None
