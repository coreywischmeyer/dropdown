import quote_boxes
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Turn a clue into a dropdown puzzle.")
    parser.add_argument('line_length', type=int, help="How long do you want each line of the puzzle to be?")
    parser.add_argument('clue', type=str, help="The clue you want to be scrambled, in parentheses!")
    parser.add_argument('output_prefix', type=str, help="What should the output pdf be called, the answer will be saved as prefix.answer.pdf")
    args = parser.parse_args()
    qb = quote_boxes.QuoteBox(args.clue,line_length=args.line_length)
    qb.to_latex(filename=args.output_prefix)
    qb.to_latex(filename=(args.output_prefix + ".answer"), answer_key=True)