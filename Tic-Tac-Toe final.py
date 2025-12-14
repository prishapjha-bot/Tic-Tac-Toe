from tkinter import *
import random
root = Tk()                   
root.title("Tic-Tac-Toe")

# --- THEME  ---
DEEP_BG = "#1A0A3A" 
GRID_GLOW_COLOR = "#33CCFF" 
BUTTON_BG = DEEP_BG 
X_COLOR = "#FF6633"  
O_COLOR = "#99FFFF"  
FONT_STYLE = ("Arial", 60, "bold") 
ANIMATION_DELAY_MS = 300
WINNER_MESSAGE_FONT = ("Impact", 20, "bold") 
WINNING_HIGHLIGHT = "#FF00FF" 

MODE_BUTTON_FG_1 = X_COLOR       
MODE_BUTTON_FG_2 = O_COLOR       
MODE_BUTTON_FONT = ("Impact", 20, "bold") 
CHAR_BUTTON_FONT = ("Impact", 40, "bold") 
MODE_BUTTON_ACTIVE_BG = "#3A0A6A"
MODE_BUTTON_RELIEF = "flat"       

root.configure(bg=DEEP_BG)

# --- GLOBAL VARIABLES ---
player_1 = ""
player_2 = ""
var = IntVar()
player_mode = IntVar()
all_buttons = []
board_current = ["","","","","","","","",""]
to_win = [
    [0,1,2], [3,4,5], [6,7,8],
    [0,3,6], [1,4,7], [2,5,8],
    [0,4,8], [2,4,6]
]
current_turn = "player_1"
game_active = True 

# --- CORE FUNCTIONS ---

def screen_clearer():
    for widget in root.winfo_children():
        widget.destroy()

def start_new_game():
    global board_current, all_buttons, current_turn, game_active
    board_current = ["","","","","","","","",""]
    all_buttons = []
    current_turn = "player_1"
    game_active = True
    screen_clearer()
    setup_mode_selection_screen() 

def flash_winner_label(label_widget, winner, color_index=0):
    if not game_active:
        return
    colors = [X_COLOR, O_COLOR] 
    next_color = colors[color_index % 2]
    
    label_widget.config(fg=next_color)
    
    label_widget.after(ANIMATION_DELAY_MS, lambda: flash_winner_label(label_widget, winner, color_index + 1))


def create_grid_button(parent_frame, command, row_idx, col_idx):
    cell_frame = Frame(parent_frame, bg=GRID_GLOW_COLOR, padx=6, pady=6) 
    cell_frame.grid(row=row_idx, column=col_idx, sticky="nsew")

    btn = Button(
        cell_frame,
        padx=40, pady=40,
        bg=BUTTON_BG,       
        fg="white", 
        border=0,           
        relief="flat",      
        activebackground=MODE_BUTTON_ACTIVE_BG,
        command=command
    )
    btn.pack(expand=True, fill="both") 
    
    return btn

def display_end_game_message(message, winner=None):
    global game_active
    game_active = False 

    Label1 = Label(
        root,
        text=message,
        font=WINNER_MESSAGE_FONT, 
        bg=DEEP_BG,
        fg=X_COLOR  
    )
    Label1.grid(row=1, column=1, columnspan=3, sticky="nsew", pady=10)
    
    if winner:
        winning_line = next((line for line in to_win if board_current[line[0]] == board_current[line[1]] == board_current[line[2]]), None)
        
        if winning_line:
            highlight_color = WINNING_HIGHLIGHT 
            
            for index in winning_line:
                all_buttons[index].master.config(bg=highlight_color) 
                all_buttons[index].config(fg=highlight_color, bg=BUTTON_BG)
                
        root.update_idletasks()
        root.update()
    
    flash_winner_label(Label1, winner or "TIE")
    
    reset_button = Button(
        root, 
        text="START NEW GAME", 
        command=start_new_game, 
        font=("Impact", 18, "bold"), 
        bg=MODE_BUTTON_ACTIVE_BG,
        fg=GRID_GLOW_COLOR,
        activebackground=DEEP_BG
    )
    reset_button.grid(row=6, column=2, pady=20)


def check_winner():
    global board_current
    
    # --- FIND WINNER ---
    for line in to_win:
        if board_current[line[0]] == board_current[line[1]] == board_current[line[2]] and board_current[line[0]] != "":
            winner = board_current[line[0]]
            display_end_game_message(f"🎉 GAME OVER! WINNER IS {winner} 🎉", winner)
            for btn in all_buttons:
                btn.config(state="disabled")
            return True 

    # --- CHECK TIE ---
    if "" not in board_current:
        display_end_game_message("🤝 GAME OVER! IT'S A TIE! 🤝")
        for btn in all_buttons:
            btn.config(state="disabled")
        return True
    
    return False

def find_best_move(player):
    for line in to_win:
        count=0
        empty_spot = -1
        for id in line:
            if board_current[id] == player:
                count+=1
            elif board_current[id] == "":
                empty_spot = id
        if count==2 and empty_spot !=-1:
            return(empty_spot)
    return None

def computer_turn():
    global board_current, all_buttons, player_1, player_2
    
    comp_color = O_COLOR if player_2 == "O" else X_COLOR
    
    win_move = find_best_move(player_2) 
    block_move = find_best_move(player_1)
    
    if win_move != None:                                 #priority 1: if win possible then win
        move_id = win_move
    elif block_move != None:                             #priority 2: if block possible then block
        move_id = block_move
    elif board_current[4] == "":                         #priority 3: if center possible then take center
        move_id = 4
    else:
        moves = [0, 2, 6, 8, 1, 3, 5, 7]             
        random.shuffle(moves[:4])                        #priority 4: if corner possible then take corner
        random.shuffle(moves[4:])                        #priority 5 : take any side
        
        move_id = next((i for i in moves if board_current[i] == ""), None)
        
    if move_id is not None:
        board_current[move_id] = player_2
        all_buttons[move_id].config(text=player_2, fg=comp_color, font=FONT_STYLE, state='disabled')


def click(btn,id):
    global board_current,player_1          
    
    player_color = X_COLOR if player_1 == "X" else O_COLOR
    
    if board_current[id] != "" or not game_active:
        return
        
    btn.config(text=player_1, fg=player_color, font=FONT_STYLE, state='disabled') 
    board_current[id] = player_1
    
    if check_winner():
        return
    
    if "" in board_current:
        computer_turn()
        check_winner() 


def two_player_click(btn,id):
    global current_turn, board_current, player_1, player_2
    
    if board_current[id] != "" or not game_active:
        return  

    if current_turn == "player_1":
        board_current[id] = player_1
        current_color = X_COLOR if player_1 == 'X' else O_COLOR
        btn.config(text=player_1, fg=current_color, font=FONT_STYLE, state="disabled")
        current_turn = "player_2"
    else:
        board_current[id] = player_2
        current_color = X_COLOR if player_2 == 'X' else O_COLOR
        btn.config(text=player_2, fg=current_color, font=FONT_STYLE, state="disabled")
        current_turn = "player_1"
    
    check_winner()

# ---LAYOUT FUNCTIONS ---

def setup_game_board(func):
    screen_clearer()
    
    grid_container = Frame(root, bg=DEEP_BG)
    grid_container.grid(row=3, column=1, columnspan=3, sticky="nsew", padx=20, pady=20)
    
    for i in range(3):
        grid_container.grid_rowconfigure(i, weight=1)
        grid_container.grid_columnconfigure(i, weight=1)
    
    root.grid_rowconfigure(3, weight=1)
    for i in range(1, 4):
        root.grid_columnconfigure(i, weight=1)
    
    func(grid_container)

def singe_player_mode(parent_frame):
    global all_buttons
    all_buttons.clear()
    
    buttons = [
        create_grid_button(parent_frame, lambda i=i: click(all_buttons[i], i), r, c)
        for i, (r, c) in enumerate([(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)])
    ]
    all_buttons.extend(buttons)

def two_player_mode(parent_frame):
    global all_buttons
    all_buttons.clear()
    
    buttons = [
        create_grid_button(parent_frame, lambda i=i: two_player_click(all_buttons[i], i), r, c)
        for i, (r, c) in enumerate([(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)])
    ]
    all_buttons.extend(buttons)

def set_character_and_start(game_mode_func):
    global player_1, player_2, var
    if var.get() == 1:
        player_1="X"
        player_2="O"
    else:
        player_1="O"
        player_2="X"
    
    setup_game_board(game_mode_func)


def setup_character_selection_screen():
    
    screen_clearer() 

    mode = player_mode.get()
    
    label_options = {"fg": "white", "bg": DEEP_BG, "font": ("Impact", 18, "bold")}
    
    radio_options = {
        "bg": DEEP_BG, 
        "selectcolor": DEEP_BG, 
        "indicatoron": 0, 
        "padx": 20, 
        "pady": 10, 
        "activebackground": MODE_BUTTON_ACTIVE_BG,
        "font": CHAR_BUTTON_FONT,
        "relief": "flat",
        "highlightthickness": 2
    }

    if mode == 1:
        text_label = "CHOOSE YOUR CHARACTER:"
        start_func = singe_player_mode
    else:
        text_label = "PLAYER 1: CHOOSE YOUR CHARACTER:"
        start_func = two_player_mode
        
    # --- Layout ---
    Label(root, text=text_label, **label_options).grid(row=1, column=0, columnspan=2, pady=30)
    
    # X Button
    rx = Radiobutton(root, text="X", variable=var, value=1, command=lambda: set_character_and_start(start_func), **radio_options, fg=X_COLOR, highlightbackground=X_COLOR)
    rx.grid(row=2, column=0, sticky="ew", padx=20)
    
    # O Button
    ro = Radiobutton(root, text="O", variable=var, value=2, command=lambda: set_character_and_start(start_func), **radio_options, fg=O_COLOR, highlightbackground=O_COLOR)
    ro.grid(row=2, column=1, sticky="ew", padx=20)
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)


def setup_mode_selection_screen():
    
    mode_frame = Frame(root, bg=DEEP_BG, padx=30, pady=30)
    mode_frame.pack(expand=True, fill="both") 

    Label(mode_frame, text="SELECT GAME MODE", fg="white", bg=DEEP_BG, font=("Impact", 30, "bold")).pack(pady=30)

    # Helper for mode buttons
    def create_mode_radio(text, value, fg_color):
        return Radiobutton(
            mode_frame,
            text=text,
            variable=player_mode,
            value=value,
            command=setup_character_selection_screen, 
            fg=fg_color,             
            bg=DEEP_BG,
            activebackground=MODE_BUTTON_ACTIVE_BG,
            selectcolor=DEEP_BG,
            font=MODE_BUTTON_FONT,
            padx=30, pady=20,
            relief=MODE_BUTTON_RELIEF,
            indicatoron=0, 
            width=20,
            border=5,
            highlightbackground=fg_color,
            highlightthickness=2
        )

    create_mode_radio(" VS COMPUTER ", 1, MODE_BUTTON_FG_1).pack(pady=20)
    create_mode_radio(" VS FRIEND (2P) ", 2, MODE_BUTTON_FG_2).pack(pady=20)

# -------------------------------------------------------------------------------------------------------------------------------------------
setup_mode_selection_screen() 
root.protocol("WM_DELETE_WINDOW", root.destroy) 
root.mainloop()