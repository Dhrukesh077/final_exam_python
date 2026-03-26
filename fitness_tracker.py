# ==============================
# IMPORT LIBRARIES
# ==============================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ==============================
# FITNESS TRACKER CLASS
# ==============================

class FitnessTracker:

    def __init__(self):
        """
        Constructor:
        - Loads existing CSV file
        - OR creates a new one if not found
        """

        self.file_name = "fitness_activities.csv"

        try:
            self.data = pd.read_csv(self.file_name)

        except FileNotFoundError:
            # Create empty dataset if file not found
            self.data = pd.DataFrame(columns=[
                "Date",
                "Activity Type",
                "Duration (Minutes)",
                "Calories Burned"
            ])
            self.data.to_csv(self.file_name, index=False)

    # ==============================
    # ADD NEW ACTIVITY
    # ==============================

    def log_activity(self, activity_type, duration, calories):
        """
        Adds a new fitness activity to dataset
        """

        # Input validation
        if duration <= 0 or calories <= 0:
            print("❌ Invalid input! Values must be positive.")
            return

        # Create new entry
        new_entry = {
            "Date": pd.Timestamp.today().strftime('%Y-%m-%d'),
            "Activity Type": activity_type,
            "Duration (Minutes)": duration,
            "Calories Burned": calories
        }

        # Append and save
        self.data = pd.concat(
            [self.data, pd.DataFrame([new_entry])],
            ignore_index=True
        )

        self.data.to_csv(self.file_name, index=False)

        print("✅ Activity added successfully!")

    # ==============================
    # CALCULATE METRICS
    # ==============================

    def calculate_metrics(self):
        """
        Calculates total calories, total duration, and average duration
        """

        if self.data.empty:
            print("⚠️ No data available!")
            return

        total_calories = np.sum(self.data["Calories Burned"])
        total_duration = np.sum(self.data["Duration (Minutes)"])
        avg_duration = np.mean(self.data["Duration (Minutes)"])

        print("\n📊 FITNESS METRICS")
        print("🔥 Total Calories Burned:", total_calories)
        print("⏱️ Total Duration:", total_duration, "minutes")
        print("📉 Average Duration:", round(avg_duration, 2), "minutes")

    # ==============================
    # FILTER ACTIVITIES
    # ==============================

    def filter_activities(self, activity_type):
        """
        Filters activities based on type
        """

        filtered = self.data[
            self.data["Activity Type"].str.lower() == activity_type.lower()
        ]

        if filtered.empty:
            print("⚠️ No matching activity found.")
        else:
            print("\n📋 Filtered Data:")
            print(filtered)

    # ==============================
    # GENERATE REPORT
    # ==============================

    def generate_report(self):
        """
        Displays statistical summary of dataset
        """

        if self.data.empty:
            print("⚠️ No data available!")
            return

        print("\n📄 FULL REPORT")
        print(self.data.describe())

    # ==============================
    # VISUALIZATIONS
    # ==============================

    def plot_bar_chart(self):
        """
        Bar chart: Time spent on each activity
        """

        if self.data.empty:
            print("⚠️ No data to plot!")
            return

        plt.figure(figsize=(8, 5))

        self.data.groupby("Activity Type")["Duration (Minutes)"].sum().plot(kind='bar')

        plt.title("Time Spent on Activities")
        plt.xlabel("Activity Type")
        plt.ylabel("Minutes")

        plt.savefig("bar_chart.png")   # Save image
        plt.show()

    def plot_line_graph(self):
        """
        Line graph: Calories burned over time
        """

        if self.data.empty:
            print("⚠️ No data to plot!")
            return

        plt.figure(figsize=(8, 5))

        self.data["Date"] = pd.to_datetime(self.data["Date"])
        self.data = self.data.sort_values("Date")

        plt.plot(self.data["Date"], self.data["Calories Burned"], marker='o')

        plt.title("Calories Burned Over Time")
        plt.xlabel("Date")
        plt.ylabel("Calories")
        plt.xticks(rotation=45)

        plt.savefig("line_graph.png")
        plt.show()

    def plot_pie_chart(self):
        """
        Pie chart: Distribution of activities
        """

        if self.data.empty:
            print("⚠️ No data to plot!")
            return

        plt.figure(figsize=(6, 6))

        self.data["Activity Type"].value_counts().plot(
            kind='pie',
            autopct='%1.1f%%'
        )

        plt.title("Activity Distribution")
        plt.ylabel("")

        plt.savefig("pie_chart.png")
        plt.show()

    def plot_heatmap(self):
        """
        Heatmap: Correlation between duration and calories
        """

        if self.data.empty:
            print("⚠️ No data to plot!")
            return

        plt.figure(figsize=(6, 4))

        correlation = self.data[
            ["Duration (Minutes)", "Calories Burned"]
        ].corr()

        sns.heatmap(correlation, annot=True)

        plt.title("Correlation Heatmap")

        plt.savefig("heatmap.png")
        plt.show()


# ==============================
# MAIN PROGRAM (MENU)
# ==============================

tracker = FitnessTracker()

while True:

    print("\n========== FITNESS TRACKER ==========")
    print("1. Add Activity")
    print("2. Show Metrics")
    print("3. Filter Activities")
    print("4. Generate Report")
    print("5. Show Visualizations")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        activity = input("Enter activity (Running/Yoga/Cycling): ")

        try:
            duration = int(input("Enter duration (minutes): "))
            calories = int(input("Enter calories burned: "))
            tracker.log_activity(activity, duration, calories)

        except ValueError:
            print("❌ Please enter valid numbers!")

    elif choice == "2":
        tracker.calculate_metrics()

    elif choice == "3":
        activity = input("Enter activity type: ")
        tracker.filter_activities(activity)

    elif choice == "4":
        tracker.generate_report()

    elif choice == "5":
        tracker.plot_bar_chart()
        tracker.plot_line_graph()
        tracker.plot_pie_chart()
        tracker.plot_heatmap()

    elif choice == "6":
        print("👋 Exiting... Stay Fit!")
        break

    else:
        print("❌ Invalid choice! Please try again.")