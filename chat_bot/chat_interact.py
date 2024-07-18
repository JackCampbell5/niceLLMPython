import time

import dill as pickle
from chat import Chat
import tkinter as tk
from tkinter import ttk, font, filedialog
from datetime import datetime
import os, sys, subprocess


class ChatInteract:
    def __init__(self):
        self.demo_mode = False
        # Values of the program
        self.options = {"Save Chat": False,
                        "Save JSON": True,
                        "Save Sources": True,
                        "Print Sources": True}
        self.default_padx = 10
        self.elements = {}
        self.starting_text = "Please describe the json trajectory you would like the LLM to create:\n"
        # The window
        self.window = tk.Tk()
        self.font_size = 18
        self.font = font.Font(size=self.font_size)
        # Params for chat
        self.chat = Chat(debug=True)
        self.active_response = None

        # Create the screen
        self.create_screen()
        self.window.mainloop()

    def create_screen(self):
        # Sets the resolution of the window
        self.window.geometry('1200x700')

        # Set Title of window
        self.window.title("NICE Large Language Model")

        # Configure grid to make it expandable
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # Welcome text at top
        self.elements["title"] = tk.Label(self.window, text="Welcome to the NICE Large Language Model",
                                          font=('', int(self.font_size * 1.75)))
        self.elements["title"].grid(row=0, column=0, columnspan=100, padx=self.default_padx, pady=(20, 5))

        self.create_scrolling_text_view()

        # Create a frame for the input and button
        input_frame = tk.Frame(self.window)
        input_frame.grid(row=3, column=0, columnspan=100, padx=self.default_padx, pady=(5, 20), sticky='ew')

        input_frame.grid_columnconfigure(1, weight=1)  # Make the first column (entry) expandable

        self.elements["clear_chat"] = tk.Button(input_frame, text="Clear", font=self.font,
                                                command=self.clear_chat)
        self.elements["clear_chat"].grid(row=0, column=0, padx=self.default_padx, pady=(1, 10), sticky='w',
                                         ipadx=self.default_padx, ipady=5)
        self.elements["prompt_input"] = tk.Entry(input_frame, font=self.font)
        self.elements["prompt_input"].grid(row=0, column=1, padx=self.default_padx, sticky='ew')
        self.elements["prompt_input"].bind("<Return>", self.submit_prompt_event)

        self.elements["prompt_submit"] = tk.Button(input_frame, text="Submit", font=self.font,
                                                   command=self.submit_prompt)
        self.elements["prompt_submit"].grid(row=0, column=2, padx=self.default_padx, pady=(1, 10), sticky='w',
                                            ipadx=5, ipady=5)
        # Option menu variable
        option_var = tk.StringVar(input_frame)
        option_var.set("Actions")  # default value
        self.elements["option_menu"] = tk.OptionMenu(input_frame, option_var, *self.options.keys(),
                                                     command=self._option_selected)
        self.elements["option_menu"].config(font=self.font)
        self.elements["option_menu"].grid(row=0, column=3, padx=self.default_padx, pady=(1, 10), sticky='w',
                                          ipadx=5, ipady=5)
        self.update_menu()

        if self.demo_mode:
            # Create a frame for the left buttons
            left_button_frame = tk.Frame(self.window)
            left_button_frame.grid(row=2, column=0, sticky='n', padx=self.default_padx, pady=self.default_padx)
            # # Into Label and directors
            self.elements["title_label"] = tk.Label(left_button_frame, text="Try an example prompt:", font=self.font)
            self.elements["title_label"].grid(row=0, column=0, columnspan=100, padx=self.default_padx, pady=(5, 20),
                                              sticky='W')

            text = [""] * 5
            text[0] = ("Create a json trajectory with prefix angleChecks...sample angle from 1 to 1.96 with a step of "
                       "0.08...")
            text[1] = ("Create a json trajectory with prefix apertureChecks...sets slitAperture1 to 0.4 times the "
                       "sample angle...")
            text[2] = "Create a json trajectory with prefix mb111 with description “5.4kG mq PSD..."
            text[3] = ("Create a json trajectory with prefix live.sample.name...loops through sampleAngle from -1 to 2 "
                       "with step of 0.0075...")
            text[4] = ("Create a json trajectory for the magik instrument that that loop through sample angle from 2 "
                       "to 4 with a step of 0.1 that sets slitAperture1 to 0.4 times the sample angle")

            # Add four buttons to the left side
            self.elements["button0"] = tk.Button(left_button_frame, text=text[0], font=self.font,
                                                 command=lambda: self.question_buttons_submit(0), width=30,
                                                 wraplength=self.font_size * 23)
            self.elements["button0"].grid(row=1, column=0, pady=5, ipadx=5, ipady=5)
            self.elements["button1"] = tk.Button(left_button_frame, text=text[1], font=self.font,
                                                 command=lambda: self.question_buttons_submit(1), width=30,
                                                 wraplength=self.font_size * 23)
            self.elements["button1"].grid(row=2, column=0, pady=5, ipadx=5, ipady=5)
            self.elements["button2"] = tk.Button(left_button_frame, text=text[2], font=self.font,
                                                 command=lambda: self.question_buttons_submit(2), width=30,
                                                 wraplength=self.font_size * 23)
            self.elements["button2"].grid(row=3, column=0, pady=5, ipadx=5, ipady=5)
            self.elements["button3"] = tk.Button(left_button_frame, text=text[3], font=self.font,
                                                 command=lambda: self.question_buttons_submit(3), width=30,
                                                 wraplength=self.font_size * 23)
            self.elements["button3"].grid(row=4, column=0, pady=5, ipadx=5, ipady=5)
            self.elements["button4"] = tk.Button(left_button_frame, text=text[4], font=self.font,
                                                 command=lambda: self.question_buttons_submit(4), width=30,
                                                 wraplength=self.font_size * 23)
            self.elements["button4"].grid(row=5, column=0, pady=5, ipadx=5, ipady=5)

    def clear_chat(self):
        self.chat.clear_chat()
        self.update_text_view(bold=self.starting_text, reset=True)

    def submit_prompt_event(self, event):
        self.submit_prompt()

    def submit_prompt(self):
        self.elements["prompt_submit"].config(state=tk.DISABLED)
        prompt = self.elements["prompt_input"].get()
        self.elements["prompt_input"].delete(0, tk.END)
        self.update_text_view(bold="\n\nUser:\n", new_text=prompt)

        self.active_response = self.chat.send_message(message=prompt)
        # documents_dir = os.path.expanduser('~\\Documents\\niceLLM\\niceAiResults')
        # file_path = os.path.join(documents_dir, "chat.pkl")
        # with open(file_path, 'wb') as file:
        #     pickle.dump(self.chat, file)
        # file_path1 = os.path.join(documents_dir, "chat.pkl")
        # with open(file_path1, 'wb') as file:
        #     pickle.dump(self.elements["text"], file)
        self.update_text_view(bold="\n\nLLM:\n", new_text=self.active_response)

        # Save JSON
        start = self.active_response.find("{")
        end = self.active_response.rfind("}")
        prefix = self.active_response.find("filePrefix")
        if start == -1 or end == -1 or prefix == -1:
            text = "No json to save. Try printing sources from the actions menu."
            self.update_text_view(bold="\n\nSystem:", red_text=text)
        else:
            self.options["Save JSON"] = False

        sources = self.chat.get_sources()
        if sources is None:
            text = "No sources to save. If you need sources try another prompt."
            self.update_text_view(bold="\n\nSystem:", red_text=text)
        else:
            self.options["Save Sources"] = False
            self.options["Print Sources"] = False

        self.update_menu()

        self.elements["prompt_submit"].config(state=tk.NORMAL)

    def update_menu(self):
        menu = self.elements["option_menu"]["menu"]
        menu.delete(0, "end")
        for name, state in self.options.items():
            state = "disabled" if state else "normal"
            menu.add_command(label=name, state=state, command=lambda opt=name: self._option_selected(opt))

    def _option_selected(self, option):
        if option == "Save Chat":
            self._save_chat()
        elif option == "Save JSON":
            self._download_json()
        elif option == "Save Sources":
            self.submit_sources()
        elif option == "Print Sources":
            self.submit_sources(save=False)

    def _save_chat(self):
        text = self.elements["text"].get(1.0, tk.END)
        self._save_to_file(text=text, file_name="chat_log")

    def _download_json(self):
        print("Saving JSON")
        name = "JSON"
        text_to_save = self.active_response[self.active_response.find("@#@$@%@^@") + 9:self.active_response.rfind(
            "@#@$@%@^@")]
        jnum = text_to_save.find("'''json")
        if jnum != -1:
            text_to_save = text_to_save[jnum + 7:]

        jnum = text_to_save.find("'''")
        if jnum != -1:
            text_to_save = text_to_save[:jnum]
        prefix = text_to_save.find("filePrefix")
        if prefix != -1:
            prefix = text_to_save[prefix + 11:]
            prefix = prefix[prefix.find("\"") + 1:]
            prefix = prefix[:prefix.find("\"")]
            name = prefix + "_" + name
        self._save_to_file(text=text_to_save, file_name=name)

    def submit_sources(self, save=True):
        print("Sources Saving:", save)
        sources = self.chat.get_sources()
        if sources is None:
            text = "No sources to save. Try another prompt."
            self.update_text_view(bold="\n\nSystem:", red_text=text)
        if save:
            self._save_to_file(text="\n\n" + sources, file_name="sources")
        else:
            self.update_text_view(bold="\n\nSystem: Printing out sources \n", new_text=sources)

    def _save_to_file(self, text, file_name):
        today_date = datetime.today().strftime('%Y.%m.%d_%H.%M')  # Get today's date in YYYY-MM-DD format
        default_filename = test_filename = f"{file_name}_(niceLLM_{today_date}).txt"
        initial_dir = os.path.expanduser('~\\Documents\\niceLLM\\niceAiResults')
        if not os.path.isdir(initial_dir):
            os.mkdir(initial_dir)

        file_counter = 0
        base_name, extension = os.path.splitext(default_filename)
        while os.path.exists(os.path.join(initial_dir, test_filename)):
            test_filename = f"{base_name}({file_counter}){extension}"
            file_counter += 1
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 initialfile=test_filename,
                                                 initialdir=initial_dir,
                                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(text)
            self.update_text_view(bold="\n\nSystem:", new_text=f"{file_name} saved:\n", link=file_path)

    def open_file(self, event):
        # Get the text of the hyperlink tag
        index = self.elements["text"].index("@%s,%s" % (event.x, event.y))
        file_path = self.elements["text"].get("%s linestart" % index, "%s lineend" % index)
        try:
            if os.name == 'nt':  # Windows
                os.startfile(file_path)
            elif os.name == 'posix':  # macOS and Linux
                if sys.platform == 'darwin':  # macOS
                    subprocess.call(['open', file_path])
                else:  # Linux
                    subprocess.call(['xdg-open', file_path])
        except Exception as e:
            self.update_text_view(bold="\n\nSystem:", red_text=f"Failed to open file: {e}\n")

    def question_buttons_submit(self, num):
        self.clear_chat()
        prompt = ""
        if num == 0:
            prompt = ("Create a json trajectory with prefix angleChecks with description “this is a file that "
                      "checks angle” that loop through sample angle from 1 to 1.96 with a step of 0.08 and "
                      "detector angle from 2 to 3.92 with a step of 0.16. “init” section should contain a count "
                      "against TIME and time and monitor counters at 40 and nothing else.")
        elif num == 1:
            prompt = ("Create a json trajectory with prefix apertureChecks with description “this loops through "
                      "apertures” that loop through sample angle from 2 to 4 with a step of 0.1 that sets "
                      "slitAperture1 to 0.4 times the sample angle. “init” section should contain a count against "
                      "TIME and set prefac to 2 and nothing else.")
        elif num == 2:
            prompt = ("Create a json trajectory with prefix mb111 with description “5.4kG mq PSD” that loop through "
                      "detector angle from 0.8 to 2 with a step of 0.1 as well as looping through slitAperture1 from "
                      "1 to 1 with step of 0. “init” section should contain down set to down and up set to up and a "
                      "count against TIME.")
        elif num == 3:
            prompt = ("Create a json trajectory with prefix live.sample.name with description “'transverse 5+5um "
                      "stripes'” that loops through sampleAngle from -1 to 2 with step of 0.0075. “init” section "
                      "should contain detector angle set to 1.24 and a count against TIME.")
        else:
            prompt = ("Create a json trajectory for the magik instrument that that loop through sample angle from 2 to "
                      "4 with a step of 0.1 that sets slitAperture1 to 0.4 times the sample angle")
        self.elements["prompt_input"].delete(0, tk.END)
        self.elements["prompt_input"].insert(0, prompt)
        self.submit_prompt()

    def create_scrolling_text_view(self):
        # Create the main frame
        main_frame = tk.Frame(self.window)
        main_frame.grid(row=2, column=1, columnspan=100, padx=self.default_padx, pady=(5, 20), sticky='nsew')

        # Create a Scrollbar and attach it to the Text widget
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Text widget
        self.elements["text"] = tk.Text(main_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set, state=tk.DISABLED,
                                        font=self.font)
        self.elements["text"].pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.elements["text"].tag_configure("bold", font=font.Font(weight="bold", size=self.font_size))
        self.elements["text"].tag_configure("red", font=font.Font(weight="bold", size=self.font_size), foreground="red")
        self.elements["text"].tag_config('link', foreground='blue', underline=True, font=font.Font(size=self.font_size))
        self.elements["text"].tag_bind('link', '<Enter>', lambda e: e.widget.config(cursor='hand2'))
        self.elements["text"].tag_bind('link', '<Leave>', lambda e: e.widget.config(cursor=''))
        self.elements["text"].tag_bind('link', '<Button-1>', self.open_file)

        # Configure the Text widget to use the Scrollbar
        self.elements["text"].configure(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.elements["text"].yview)
        self.update_text_view(bold=self.starting_text)

    def update_text_view(self, bold="", new_text="", red_text="", link="", reset=False):
        # Clear the current content
        self.elements["text"].config(state=tk.NORMAL)
        if reset:
            self.elements["text"].delete(1.0, tk.END)
        # Insert the new content
        self.elements["text"].insert(tk.END, bold, 'bold', red_text, 'red', new_text, '', link, 'link')

        self.elements["text"].see(tk.END)
        self.elements["text"].config(state=tk.DISABLED)
        self.window.update_idletasks()


chat = ChatInteract()
