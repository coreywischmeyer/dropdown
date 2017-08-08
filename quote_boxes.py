import re
import random
class QuoteBox:

    def __init__(self, quote, line_length=22):
        self.quote = self._clean_quote(quote)
        self.line_length = line_length
        self.puzzle = self._build_puzzle()
        self.answer

    def _build_puzzle(self):
        quote_box = list()

        self._pad_quote()
        start = 0
        for i in range(0, int(len(self.quote) / self.line_length)):
            quote_box.append(list(self.quote[start:start + self.line_length]))
            start = start + self.line_length

        self.answer = quote_box

        vertical_boxes = list()
        for i in range(0, self.line_length):
            vertical_slice = [x[i] for x in quote_box]
            vertical_slice = sorted(vertical_slice, reverse=True)
            if " " in vertical_slice:
                index = vertical_slice.index(" ")
                x = vertical_slice[:index]
                random.shuffle(x)
                vertical_slice[:index] = x
            else:
                random.shuffle(vertical_slice)
            vertical_boxes.append(vertical_slice)
        puzzle = list()
        for i in range(0, int(len(self.quote) / self.line_length)):
            puzzle_line = list()
            for j in range(0, self.line_length):
                puzzle_line.append(vertical_boxes[j][i])
            puzzle.append(puzzle_line)
        return puzzle

    def to_latex(self, filename="out", answer_key=False):
        tex_filename = "{}.tex".format(filename)
        pdf_filename = "{}.pdf".format(filename)
        from pprint import pprint
        latex_answer_box = ""
        latex_puzzle_box = ""

        for line_index, line in enumerate(self.puzzle):
            for letter_index, letter in enumerate(line):
                line_modifier = ""
                cell_modifier = ""
                if line_index is 0:
                    line_modifier = "t"
                if letter_index is 0:
                    cell_modifier = "l"
                if letter_index is len(line) - 1:
                    cell_modifier = "r"
                modifier = cell_modifier + line_modifier
                if letter is " ":
                    latex_answer_box += "|[][{}f]{}".format(modifier, "x")
                else:
                    latex_answer_box += "|[][{}fS]{}".format(modifier, letter)
            latex_answer_box += "|.\n"
        for line_index, line in enumerate(self.answer):
            for letter_index, letter in enumerate(line):
                line_modifier = ""
                cell_modifier = ""
                if answer_key is True:
                    cell_modifier += "S"
                if line_index is 0:
                    line_modifier += "t"
                if letter_index is 0:
                    cell_modifier += "l"
                if letter_index is len(line) - 1:
                    cell_modifier += "r"
                if line_index is len(self.answer) - 1:
                    line_modifier += "b"
                modifier = cell_modifier + line_modifier
                if letter is " ":
                    latex_answer_box += "|[][{}f]*".format(modifier)
                else:
                    latex_answer_box += "|[][{}f]{}".format(modifier,letter)
            latex_answer_box += "|.\n"

        #Start Jinja
        from jinja2 import Environment, PackageLoader, select_autoescape
        import os
        import subprocess
        env = Environment(
            loader=PackageLoader('dropdown')
        )
        #Tex doesn't like '{{' and '}}'
        env.variable_start_string = '((('
        env.variable_end_string = ')))'
        template = env.get_template('quote_boxes.tex')
        template_out = template.render(line_length=self.line_length,
                                       num_lines=int(len(self.quote) / self.line_length * 2),
                                       puzzle_string=latex_puzzle_box + latex_answer_box)

        with open(tex_filename, 'w') as f:
            f.write(template_out)

        cmd = ['pdflatex', '-interaction', 'nonstopmode', tex_filename]
        proc = subprocess.Popen(cmd)
        proc.communicate()
        retcode = proc.returncode
        if not retcode == 0:
            os.unlink(pdf_filename)
            raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))
        #os.unlink(tex_filename)
        #os.unlink('{}.log'.format(filename))


    def _pad_quote(self):
        while (len(self.quote) % self.line_length) != 0:
            self.quote += " "

    def _clean_quote(self, quote):
        letters_only = re.compile('[^a-zA-Z ]')
        return letters_only.sub('', quote).upper()

    def __str__(self):
        return self.quote

    def __repr__(self):
        return(self.quote)