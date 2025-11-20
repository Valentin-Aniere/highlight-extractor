#https://medium.com/@vinitvaibhav9/extracting-pdf-highlights-using-python-9512af43a6d


import pymupdf, sys

filename = str(sys.argv[1])
doc = pymupdf.open(filename)

# List to store all the highlighted texts
highlight_text = []
current_y=0

# loop through each page
for page in doc:

    # list to store the co-ordinates of all highlights
    highlights = []

    # loop till we have highlight annotation in the page
    annot = page.first_annot
    while annot:
        if annot.type[0] == 8:
            all_coordinates = annot.vertices
            if len(all_coordinates) == 4:
                highlight_coord = pymupdf.Quad(all_coordinates).rect
                highlights.append(highlight_coord)
            else:
                all_coordinates = [all_coordinates[x:x + 4] for x in range(0, len(all_coordinates), 4)]
                for i in range(0, len(all_coordinates)):
                    coord = pymupdf.Quad(all_coordinates[i]).rect
                    highlights.append(coord)
        annot = annot.next

    all_words = page.get_text("words")

    for h in highlights:
        #print(h[-1])
        sentence = [w[4] for w in all_words if pymupdf.Rect(w[0:4]).intersects(h)]

        # Check if the y-coordinate difference is less than the line height before joining sentences
        if current_y and h[1] - current_y < h[-1]-h[1]:
            print(h[1])
            print(current_y)
            print("yes")
            highlight_text[-1]=highlight_text[-1]+" ".join(sentence)
        else:
            highlight_text.append(" ".join(sentence))

        current_y = h[-1]




with open("highlight.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(highlight_text))
