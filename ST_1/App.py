import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

class StockPriceApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Stock Price Prediction')
        self.master.geometry('400x300')  # Set the initial window size

        self.data = pd.read_csv('Starbucks.csv')  # Update with your actual data file

        # Perform data preprocessing

        self.data = self.data[['open', 'high', 'low', 'close']]

        self.X = self.data[['open', 'high', 'low']].values
        self.y = self.data['close'].values

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=42)

        self.model = LinearRegression()
        self.model.fit(self.X_train, self.y_train)

        self.create_widgets()

    def create_widgets(self):
        self.frame = tk.Frame(self.master, padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')

        self.sliders = []  # Store sliders and associated variables
        self.slider_vars = []  # Store StringVars for text box values

        for i, column in enumerate(self.data.columns[:-1]):
            if column.lower() == 'close':  # Skip creating slider for 'close' column
                continue

            label = tk.Label(self.frame, text=column + ': ', font=('Arial', 12, 'bold'))
            label.grid(row=i, column=0, sticky='w', pady=5)

            # Create a StringVar for each slider
            var = tk.StringVar()
            var.set('0.0')  # Set initial value for text box
            self.slider_vars.append(var)

            # Slider
            slider = ttk.Scale(self.frame, from_=self.data[column].min(), to=self.data[column].max(),
                               orient="horizontal", variable=var)
            slider.grid(row=i, column=1, pady=5)
            self.sliders.append(slider)

            # Text Box
            text_box = tk.Entry(self.frame, font=('Arial', 12), textvariable=var)
            text_box.grid(row=i, column=2, padx=5, pady=5)

        predict_button = tk.Button(self.master, text='Predict Price', command=self.predict_price, font=('Arial', 14))
        predict_button.pack(pady=10)

    def predict_price(self):
        inputs = [float(var.get()) for var in self.slider_vars]
        open_price, high_price, low_price = inputs[:3]

        if low_price > high_price or open_price > high_price:
            messagebox.showerror('Input Error', 'Low or Open price cannot be greater than High price.')
        else:
            price = self.model.predict([inputs[:3]])
            messagebox.showinfo('Predicted Price', f'The predicted stock price is ${price[0]:.2f}')

if __name__ == '__main__':
    root = tk.Tk()
    app = StockPriceApp(root)
    root.mainloop()
