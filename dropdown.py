from word_games import quote_boxes

if __name__ == "__main__":
    qb = quote_boxes.QuoteBox("COME FIND OUR BALLOON AT THE TRAINWRECK SALOON",line_length=12)
    qb.to_latex()