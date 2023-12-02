import os
from tkinter import *
from collections import defaultdict

class RestaurantSearch:
    def __init__(self):
        # Initializes the RestaurantSearch class, creating the inverted index and document list
        self.inverted_index = defaultdict(list)
        self.documents = []
        self.load_and_index_files()

    def load_and_index_files(self):
        # Loads restaurant data from files and indexes them for search
        file_location = os.path.join(os.path.dirname(__file__), "restaurants")
        if not os.path.exists(file_location):
            messagebox.showerror("Error", "Restaurant folder does not exist")
            exit()

        for filename in os.listdir(file_location):
            with open(os.path.join(file_location, filename), "r") as file:
                content = file.read()
                self.documents.append(content)
                self.index_document(content)

    def index_document(self, content):
        # Creates an index of words from the document content for search functionality
        tokens = content.lower().split()
        doc_id = len(self.documents) - 1
        for token in tokens:
            cleaned_token = token.strip(".,").replace("and", "").replace("the", "")
            if doc_id not in self.inverted_index[cleaned_token]:
                self.inverted_index[cleaned_token].append(doc_id)

    def search(self, query, location):
        # Searches indexed documents based on the query and location, returning relevant results
        query_terms = query.lower().split()
        query_len = len(query_terms)
        result_list = []
        for term in query_terms:
            cleaned_term = term.strip(".,").replace("and", "").replace("the", "")
            result_list.extend(self.inverted_index[cleaned_term])

        rank_dict = {doc_id: result_list.count(doc_id) / query_len for doc_id in set(result_list)}
        ranked_results = sorted(rank_dict, key=rank_dict.get, reverse=True)

        return self.format_results(ranked_results, rank_dict, location), len(ranked_results)

    def format_results(self, ranked_results, rank_dict, location):
        # Formats the search results for display, filtering by location if specified
        output = []
        location_match_count = 0
        for doc_id in ranked_results:
            title, loc = self.documents[doc_id].split("\n")[:2]
            if location and loc != location:
                continue
            location_match_count += 1
            relevance = round(rank_dict[doc_id] * 100, 3)
            output.append(f"{title}, LOC: {loc}, relevance: {relevance}%")
        return output, location_match_count


class GUI:
    def __init__(self, master):
        # Initializes the GUI elements and sets up the main window
        self.master = master
        master.title('The Restaurant Selector')
        master.geometry("850x600")

        self.search_engine = RestaurantSearch()

        Label(master, text="What do you feel like eating today?", font=("Times", 21)).pack()
        self.query_entry = Text(master, width=40, height=5)
        self.query_entry.pack()

        Label(master, text="(Optional) Please enter a city name and the first two letters of the state. e.g., Urbana IL", font=("Times", 8)).pack()
        self.location_entry = Entry(master, width=20)
        self.location_entry.pack()

        self.results_text = Text(master, width=95, height=24)
        self.results_text.pack()

        Button(master, text="Find Restaurants", command=self.perform_search).pack()

    def perform_search(self):
        # Initiates a search when the 'Find Restaurants' button is clicked
        query = self.query_entry.get("1.0", "end").strip()
        location = self.location_entry.get().strip()
        results, total_results = self.search_engine.search(query, location)
        results, location_match_count = results

        self.results_text.delete("1.0", END)
        self.results_text.insert("1.0", f"{total_results} total results returned\n")
        if location:
            self.results_text.insert(END, f"Location Filter Applied\n{location_match_count} relevant to your specified location\n")
        else:
            self.results_text.insert(END, "No Location Filter Applied\n")
        for result in results:
            self.results_text.insert(END, result + "\n")

def main():
    # The main function to run the application
    root = Tk()
    gui = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
