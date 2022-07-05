import turtle, pandas

screen = turtle.Screen()
screen.title("U.S. States Game")
IMAGE = ("blank_states_img.gif")
screen.addshape(IMAGE)
turtle.shape(IMAGE)
CORRECT_ANSWERS = []
states_data = pandas.read_csv("50_states.csv")

FONT = ("Calibri", "12", "normal")
text = turtle.Turtle()
text.ht()
text.pu()
text.speed(0)

while len(set(CORRECT_ANSWERS)) < 50:
    answer_state = screen.textinput(
        title=f"{len(set(CORRECT_ANSWERS))}/50 States Correct", prompt="Name a state in the US")

    if answer_state is None:
        missing_states = [state for state in states_data.state if state not in CORRECT_ANSWERS]
        pandas.DataFrame(missing_states).to_scv("states_to_leaern.csv")
        screen.bye()
    elif answer_state.title() in states_data.state.to_list():
        CORRECT_ANSWERS.append(answer_state)
        coordinates = states_data[states_data.state == answer_state.title()]
        text.goto(int(coordinates.x), int(coordinates.y))
        text.write(f"{answer_state.title()}", font=FONT, align="center")

text.goto(0, 0)
text.write("YOU GUESSED ALL STATES!", font=("Calibri", "50", "normal"), align="center")

screen.mainloop()
