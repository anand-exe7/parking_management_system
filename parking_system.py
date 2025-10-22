import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json
import os
from collections import defaultdict

class ParkingManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Management System Pro")
        self.root.geometry("1200x750")
        self.root.configure(bg="#2c3e50")
        
        # Data structures
        self.parking_spots = {}
        self.parked_vehicles = {}
        self.history = []
        self.total_spots = 50
        self.rates = {"Car": 20, "Bike": 10, "Truck": 30, "SUV": 25}
        self.reserved_spots = set()
        
        # Initialize parking spots
        for i in range(1, self.total_spots + 1):
            self.parking_spots[i] = None
        
        # Load data
        self.load_data()
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        # Title
        title_frame = tk.Frame(self.root, bg="#2c3e50")
        title_frame.pack(pady=15)
        
        title = tk.Label(title_frame, text="🚗 PARKING MANAGEMENT SYSTEM PRO", 
                        font=("Arial", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
        title.pack()
        
        subtitle = tk.Label(title_frame, text="Complete Parking Solution with Advanced Analytics", 
                           font=("Arial", 11), bg="#2c3e50", fg="#95a5a6")
        subtitle.pack()
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_frame, bg="#34495e", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Park Vehicle Section
        park_label = tk.Label(left_panel, text="Park Vehicle", 
                             font=("Arial", 16, "bold"), bg="#34495e", fg="#ecf0f1")
        park_label.pack(pady=15)
        
        tk.Label(left_panel, text="Vehicle Number:", bg="#34495e", 
                fg="#ecf0f1", font=("Arial", 11)).pack(pady=5)
        self.vehicle_entry = tk.Entry(left_panel, font=("Arial", 12), width=20)
        self.vehicle_entry.pack(pady=5)
        
        tk.Label(left_panel, text="Vehicle Type:", bg="#34495e", 
                fg="#ecf0f1", font=("Arial", 11)).pack(pady=5)
        self.vehicle_type = ttk.Combobox(left_panel, values=["Car", "Bike", "Truck", "SUV"], 
                                         font=("Arial", 12), width=18, state="readonly")
        self.vehicle_type.set("Car")
        self.vehicle_type.pack(pady=5)
        
        tk.Label(left_panel, text="Owner Name:", bg="#34495e", 
                fg="#ecf0f1", font=("Arial", 11)).pack(pady=5)
        self.owner_entry = tk.Entry(left_panel, font=("Arial", 12), width=20)
        self.owner_entry.pack(pady=5)
        
        tk.Label(left_panel, text="Phone Number:", bg="#34495e", 
                fg="#ecf0f1", font=("Arial", 11)).pack(pady=5)
        self.phone_entry = tk.Entry(left_panel, font=("Arial", 12), width=20)
        self.phone_entry.pack(pady=5)
        
        park_btn = tk.Button(left_panel, text="🅿️ Park Vehicle", 
                            command=self.park_vehicle, bg="#27ae60", fg="white",
                            font=("Arial", 12, "bold"), width=18, cursor="hand2")
        park_btn.pack(pady=10)
        
        reserve_btn = tk.Button(left_panel, text="📌 Reserve Spot", 
                               command=self.reserve_spot, bg="#3498db", fg="white",
                               font=("Arial", 11), width=18, cursor="hand2")
        reserve_btn.pack(pady=5)
        
        ttk.Separator(left_panel, orient="horizontal").pack(fill=tk.X, pady=15)
        
        # Remove Vehicle Section
        remove_label = tk.Label(left_panel, text="Remove Vehicle", 
                               font=("Arial", 16, "bold"), bg="#34495e", fg="#ecf0f1")
        remove_label.pack(pady=15)
        
        tk.Label(left_panel, text="Spot Number:", bg="#34495e", 
                fg="#ecf0f1", font=("Arial", 11)).pack(pady=5)
        self.spot_entry = tk.Entry(left_panel, font=("Arial", 12), width=20)
        self.spot_entry.pack(pady=5)
        
        remove_btn = tk.Button(left_panel, text="💳 Remove & Calculate", 
                              command=self.remove_vehicle, bg="#e74c3c", fg="white",
                              font=("Arial", 12, "bold"), width=18, cursor="hand2")
        remove_btn.pack(pady=10)
        
        search_btn = tk.Button(left_panel, text="🔍 Search Vehicle", 
                              command=self.search_vehicle, bg="#9b59b6", fg="white",
                              font=("Arial", 11), width=18, cursor="hand2")
        search_btn.pack(pady=5)
        
        ttk.Separator(left_panel, orient="horizontal").pack(fill=tk.X, pady=15)
        
        # Quick Actions
        actions_label = tk.Label(left_panel, text="Quick Actions", 
                                font=("Arial", 14, "bold"), bg="#34495e", fg="#ecf0f1")
        actions_label.pack(pady=10)
        
        clear_btn = tk.Button(left_panel, text="🗑️ Clear All Data", 
                             command=self.clear_all_data, bg="#c0392b", fg="white",
                             font=("Arial", 10), width=18, cursor="hand2")
        clear_btn.pack(pady=5)
        
        export_btn = tk.Button(left_panel, text="📊 Export Report", 
                              command=self.export_report, bg="#16a085", fg="white",
                              font=("Arial", 10), width=18, cursor="hand2")
        export_btn.pack(pady=5)
        
        # Right panel
        right_panel = tk.Frame(main_frame, bg="#34495e", relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Stats Frame
        stats_frame = tk.Frame(right_panel, bg="#34495e")
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.occupied_label = tk.Label(stats_frame, text="Occupied: 0", 
                                       font=("Arial", 12, "bold"), bg="#e74c3c", 
                                       fg="white", padx=20, pady=8)
        self.occupied_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.available_label = tk.Label(stats_frame, text=f"Available: {self.total_spots}", 
                                        font=("Arial", 12, "bold"), bg="#27ae60", 
                                        fg="white", padx=20, pady=8)
        self.available_label.grid(row=0, column=1, padx=5, pady=5)
        
        self.reserved_label = tk.Label(stats_frame, text="Reserved: 0", 
                                       font=("Arial", 12, "bold"), bg="#3498db", 
                                       fg="white", padx=20, pady=8)
        self.reserved_label.grid(row=0, column=2, padx=5, pady=5)
        
        self.revenue_label = tk.Label(stats_frame, text="Today's Revenue: ₹0", 
                                      font=("Arial", 12, "bold"), bg="#f39c12", 
                                      fg="white", padx=20, pady=8)
        self.revenue_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)
        
        # Tabs
        tab_control = ttk.Notebook(right_panel)
        
        # Current Vehicles Tab
        current_tab = tk.Frame(tab_control, bg="#34495e")
        tab_control.add(current_tab, text="📋 Current Vehicles")
        
        tree_frame = tk.Frame(current_tab, bg="#34495e")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, 
                                columns=("Spot", "Vehicle", "Type", "Owner", "Phone", "Time"), 
                                show="headings", yscrollcommand=scrollbar.set, height=12)
        self.tree.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("Spot", text="Spot #")
        self.tree.heading("Vehicle", text="Vehicle No.")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Owner", text="Owner")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Time", text="Entry Time")
        
        self.tree.column("Spot", width=60, anchor="center")
        self.tree.column("Vehicle", width=100, anchor="center")
        self.tree.column("Type", width=70, anchor="center")
        self.tree.column("Owner", width=100)
        self.tree.column("Phone", width=100)
        self.tree.column("Time", width=130, anchor="center")
        
        # History Tab
        history_tab = tk.Frame(tab_control, bg="#34495e")
        tab_control.add(history_tab, text="📜 History")
        
        history_frame = tk.Frame(history_tab, bg="#34495e")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        hist_scrollbar = ttk.Scrollbar(history_frame)
        hist_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_tree = ttk.Treeview(history_frame, 
                                         columns=("Vehicle", "Type", "Owner", "Entry", "Exit", "Duration", "Fee"), 
                                         show="headings", yscrollcommand=hist_scrollbar.set, height=12)
        self.history_tree.pack(fill=tk.BOTH, expand=True)
        hist_scrollbar.config(command=self.history_tree.yview)
        
        self.history_tree.heading("Vehicle", text="Vehicle No.")
        self.history_tree.heading("Type", text="Type")
        self.history_tree.heading("Owner", text="Owner")
        self.history_tree.heading("Entry", text="Entry Time")
        self.history_tree.heading("Exit", text="Exit Time")
        self.history_tree.heading("Duration", text="Duration (hrs)")
        self.history_tree.heading("Fee", text="Fee (₹)")
        
        self.history_tree.column("Vehicle", width=90)
        self.history_tree.column("Type", width=60)
        self.history_tree.column("Owner", width=90)
        self.history_tree.column("Entry", width=120)
        self.history_tree.column("Exit", width=120)
        self.history_tree.column("Duration", width=90, anchor="center")
        self.history_tree.column("Fee", width=70, anchor="center")
        
        # Analytics Tab
        analytics_tab = tk.Frame(tab_control, bg="#34495e")
        tab_control.add(analytics_tab, text="📊 Analytics")
        
        analytics_frame = tk.Frame(analytics_tab, bg="#34495e")
        analytics_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        self.analytics_text = tk.Text(analytics_frame, font=("Arial", 11), 
                                      bg="#2c3e50", fg="#ecf0f1", wrap=tk.WORD, 
                                      relief=tk.FLAT, padx=15, pady=15)
        self.analytics_text.pack(fill=tk.BOTH, expand=True)
        
        # Parking Map Tab
        map_tab = tk.Frame(tab_control, bg="#34495e")
        tab_control.add(map_tab, text="🗺️ Parking Map")
        
        map_canvas_frame = tk.Frame(map_tab, bg="#34495e")
        map_canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.map_canvas = tk.Canvas(map_canvas_frame, bg="#2c3e50", highlightthickness=0)
        self.map_canvas.pack(fill=tk.BOTH, expand=True)
        
        tab_control.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Bind tab change event
        tab_control.bind("<<NotebookTabChanged>>", self.on_tab_change)
        
        # Update display
        self.update_display()
        self.draw_parking_map()
        
    def park_vehicle(self):
        vehicle_num = self.vehicle_entry.get().strip().upper()
        vehicle_type = self.vehicle_type.get()
        owner = self.owner_entry.get().strip()
        phone = self.phone_entry.get().strip()
        
        if not vehicle_num or not owner:
            messagebox.showerror("Error", "Please fill vehicle number and owner name!")
            return
        
        # Check if vehicle already parked
        for spot, data in self.parked_vehicles.items():
            if data["vehicle"] == vehicle_num:
                messagebox.showerror("Error", f"Vehicle {vehicle_num} is already parked at spot {spot}!")
                return
        
        # Find available spot
        available_spot = None
        for spot in range(1, self.total_spots + 1):
            if self.parking_spots[spot] is None and spot not in self.reserved_spots:
                available_spot = spot
                break
        
        if available_spot is None:
            messagebox.showerror("Error", "No parking spots available!")
            return
        
        # Park the vehicle
        entry_time = datetime.now()
        self.parking_spots[available_spot] = vehicle_num
        self.parked_vehicles[available_spot] = {
            "vehicle": vehicle_num,
            "type": vehicle_type,
            "owner": owner,
            "phone": phone,
            "entry_time": entry_time
        }
        
        messagebox.showinfo("Success", 
                          f"✅ Vehicle {vehicle_num} parked at spot {available_spot}\n" +
                          f"Owner: {owner}\n" +
                          f"Entry Time: {entry_time.strftime('%I:%M %p')}")
        
        # Clear entries
        self.vehicle_entry.delete(0, tk.END)
        self.owner_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        
        self.update_display()
        self.save_data()
        
    def remove_vehicle(self):
        try:
            spot_num = int(self.spot_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid spot number!")
            return
        
        if spot_num not in self.parked_vehicles:
            messagebox.showerror("Error", f"No vehicle parked at spot {spot_num}!")
            return
        
        # Get vehicle data
        data = self.parked_vehicles[spot_num]
        exit_time = datetime.now()
        duration = (exit_time - data["entry_time"]).total_seconds() / 3600
        
        # Calculate fee
        rate = self.rates[data["type"]]
        fee = max(rate, round(duration * rate, 2))
        
        # Add to history
        self.history.append({
            "vehicle": data["vehicle"],
            "type": data["type"],
            "owner": data["owner"],
            "entry_time": data["entry_time"].strftime('%Y-%m-%d %I:%M %p'),
            "exit_time": exit_time.strftime('%Y-%m-%d %I:%M %p'),
            "duration": round(duration, 2),
            "fee": fee
        })
        
        # Remove from current parking
        del self.parked_vehicles[spot_num]
        self.parking_spots[spot_num] = None
        
        messagebox.showinfo("Payment Receipt", 
                          f"🚗 Vehicle: {data['vehicle']}\n" +
                          f"👤 Owner: {data['owner']}\n" +
                          f"⏱️ Duration: {round(duration, 2)} hours\n" +
                          f"💰 Total Fee: ₹{fee}\n\n" +
                          f"Thank you for parking with us!")
        
        self.spot_entry.delete(0, tk.END)
        self.update_display()
        self.save_data()
        
    def reserve_spot(self):
        spot = simpledialog.askinteger("Reserve Spot", 
                                       f"Enter spot number to reserve (1-{self.total_spots}):",
                                       minvalue=1, maxvalue=self.total_spots)
        if spot:
            if self.parking_spots[spot] is not None:
                messagebox.showerror("Error", f"Spot {spot} is already occupied!")
            elif spot in self.reserved_spots:
                messagebox.showinfo("Info", f"Spot {spot} is already reserved!")
            else:
                self.reserved_spots.add(spot)
                messagebox.showinfo("Success", f"Spot {spot} has been reserved!")
                self.update_display()
                self.save_data()
    
    def search_vehicle(self):
        vehicle = simpledialog.askstring("Search Vehicle", "Enter vehicle number:")
        if vehicle:
            vehicle = vehicle.strip().upper()
            found = False
            for spot, data in self.parked_vehicles.items():
                if data["vehicle"] == vehicle:
                    messagebox.showinfo("Vehicle Found", 
                                      f"🚗 Vehicle: {vehicle}\n" +
                                      f"📍 Spot: {spot}\n" +
                                      f"👤 Owner: {data['owner']}\n" +
                                      f"📱 Phone: {data.get('phone', 'N/A')}\n" +
                                      f"🚙 Type: {data['type']}\n" +
                                      f"⏰ Entry: {data['entry_time'].strftime('%I:%M %p')}")
                    found = True
                    break
            
            if not found:
                messagebox.showinfo("Not Found", f"Vehicle {vehicle} is not currently parked.")
    
    def clear_all_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data? This cannot be undone!"):
            self.parked_vehicles.clear()
            self.history.clear()
            self.reserved_spots.clear()
            for i in range(1, self.total_spots + 1):
                self.parking_spots[i] = None
            self.update_display()
            self.save_data()
            messagebox.showinfo("Success", "All data has been cleared!")
    
    def export_report(self):
        report = f"PARKING MANAGEMENT SYSTEM - REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}\n"
        report += "="*60 + "\n\n"
        
        report += f"CURRENT STATUS:\n"
        report += f"Total Spots: {self.total_spots}\n"
        report += f"Occupied: {len(self.parked_vehicles)}\n"
        report += f"Available: {self.total_spots - len(self.parked_vehicles)}\n"
        report += f"Reserved: {len(self.reserved_spots)}\n\n"
        
        today_revenue = sum(h['fee'] for h in self.history 
                           if h['exit_time'].startswith(datetime.now().strftime('%Y-%m-%d')))
        report += f"Today's Revenue: ₹{today_revenue}\n"
        report += f"Total Transactions: {len(self.history)}\n\n"
        
        report += "CURRENTLY PARKED VEHICLES:\n"
        report += "-"*60 + "\n"
        for spot, data in sorted(self.parked_vehicles.items()):
            report += f"Spot {spot}: {data['vehicle']} ({data['type']}) - {data['owner']}\n"
        
        with open(f"parking_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
            f.write(report)
        
        messagebox.showinfo("Success", "Report exported successfully!")
    
    def update_display(self):
        # Update stats
        occupied = len(self.parked_vehicles)
        available = self.total_spots - occupied - len(self.reserved_spots)
        self.occupied_label.config(text=f"Occupied: {occupied}")
        self.available_label.config(text=f"Available: {available}")
        self.reserved_label.config(text=f"Reserved: {len(self.reserved_spots)}")
        
        # Calculate today's revenue
        today = datetime.now().strftime('%Y-%m-%d')
        today_revenue = sum(h['fee'] for h in self.history if h['exit_time'].startswith(today))
        self.revenue_label.config(text=f"Today's Revenue: ₹{today_revenue:.2f}")
        
        # Update current vehicles
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for spot, data in sorted(self.parked_vehicles.items()):
            self.tree.insert("", tk.END, values=(
                spot,
                data["vehicle"],
                data["type"],
                data["owner"],
                data.get("phone", "N/A"),
                data["entry_time"].strftime('%I:%M %p')
            ))
        
        # Update history
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        for record in reversed(self.history[-50:]):  # Show last 50
            self.history_tree.insert("", tk.END, values=(
                record["vehicle"],
                record["type"],
                record["owner"],
                record["entry_time"],
                record["exit_time"],
                record["duration"],
                record["fee"]
            ))
        
        # Update analytics
        self.update_analytics()
        self.draw_parking_map()
    
    def update_analytics(self):
        self.analytics_text.delete(1.0, tk.END)
        
        analytics = "📊 PARKING ANALYTICS\n"
        analytics += "="*50 + "\n\n"
        
        # Vehicle type distribution
        type_count = defaultdict(int)
        for data in self.parked_vehicles.values():
            type_count[data['type']] += 1
        
        analytics += "🚗 Current Vehicle Types:\n"
        for vtype, count in type_count.items():
            analytics += f"  • {vtype}: {count}\n"
        analytics += "\n"
        
        # Historical stats
        if self.history:
            total_revenue = sum(h['fee'] for h in self.history)
            avg_duration = sum(h['duration'] for h in self.history) / len(self.history)
            
            analytics += f"💰 Total Revenue: ₹{total_revenue:.2f}\n"
            analytics += f"📊 Total Transactions: {len(self.history)}\n"
            analytics += f"⏱️ Average Parking Duration: {avg_duration:.2f} hours\n\n"
            
            # Most common vehicle types
            hist_types = defaultdict(int)
            for h in self.history:
                hist_types[h['type']] += 1
            
            analytics += "📈 Most Parked Vehicle Types:\n"
            for vtype, count in sorted(hist_types.items(), key=lambda x: x[1], reverse=True):
                analytics += f"  • {vtype}: {count} times\n"
            analytics += "\n"
            
            # Peak usage
            analytics += "⭐ Peak Usage Statistics:\n"
            analytics += f"  • Maximum Occupancy: {max(len(self.parked_vehicles), occupied if 'occupied' in locals() else 0)}/{self.total_spots}\n"
            analytics += f"  • Occupancy Rate: {(len(self.parked_vehicles)/self.total_spots)*100:.1f}%\n"
        
        self.analytics_text.insert(1.0, analytics)
    
    def draw_parking_map(self):
        self.map_canvas.delete("all")
        
        # Calculate grid
        cols = 10
        rows = (self.total_spots + cols - 1) // cols
        
        canvas_width = self.map_canvas.winfo_width()
        canvas_height = self.map_canvas.winfo_height()
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width = 900
            canvas_height = 400
        
        cell_width = (canvas_width - 40) // cols
        cell_height = (canvas_height - 40) // rows
        cell_size = min(cell_width, cell_height, 70)
        
        start_x = (canvas_width - (cols * cell_size)) // 2
        start_y = 20
        
        spot_num = 1
        for row in range(rows):
            for col in range(cols):
                if spot_num > self.total_spots:
                    break
                
                x = start_x + col * cell_size
                y = start_y + row * cell_size
                
                # Determine color
                if self.parking_spots[spot_num] is not None:
                    color = "#e74c3c"  # Occupied - Red
                    text_color = "white"
                elif spot_num in self.reserved_spots:
                    color = "#3498db"  # Reserved - Blue
                    text_color = "white"
                else:
                    color = "#27ae60"  # Available - Green
                    text_color = "white"
                
                # Draw spot
                rect = self.map_canvas.create_rectangle(
                    x + 5, y + 5, x + cell_size - 5, y + cell_size - 5,
                    fill=color, outline="#34495e", width=2
                )
                
                # Add spot number
                self.map_canvas.create_text(
                    x + cell_size // 2, y + cell_size // 2,
                    text=str(spot_num), font=("Arial", 10, "bold"),
                    fill=text_color
                )
                
                # Add vehicle number if occupied
                if self.parking_spots[spot_num] is not None:
                    vehicle = self.parked_vehicles[spot_num]["vehicle"]
                    self.map_canvas.create_text(
                        x + cell_size // 2, y + cell_size // 2 + 15,
                        text=vehicle[:6], font=("Arial", 7),
                        fill=text_color
                    )
                
                spot_num += 1
        
        # Add legend
        legend_x = 20
        legend_y = canvas_height - 60
        
        # Available
        self.map_canvas.create_rectangle(legend_x, legend_y, legend_x + 20, legend_y + 20,
                                        fill="#27ae60", outline="#34495e", width=2)
        self.map_canvas.create_text(legend_x + 30, legend_y + 10, text="Available",
                                   anchor="w", fill="#ecf0f1", font=("Arial", 10))
        
        # Occupied
        self.map_canvas.create_rectangle(legend_x + 120, legend_y, legend_x + 140, legend_y + 20,
                                        fill="#e74c3c", outline="#34495e", width=2)
        self.map_canvas.create_text(legend_x + 150, legend_y + 10, text="Occupied",
                                   anchor="w", fill="#ecf0f1", font=("Arial", 10))
        
        # Reserved
        self.map_canvas.create_rectangle(legend_x + 240, legend_y, legend_x + 260, legend_y + 20,
                                        fill="#3498db", outline="#34495e", width=2)
        self.map_canvas.create_text(legend_x + 270, legend_y + 10, text="Reserved",
                                   anchor="w", fill="#ecf0f1", font=("Arial", 10))
    
    def on_tab_change(self, event):
        # Redraw parking map when tab is switched
        self.root.after(100, self.draw_parking_map)
    
    def save_data(self):
        data = {
            "parked_vehicles": {
                spot: {
                    "vehicle": info["vehicle"],
                    "type": info["type"],
                    "owner": info["owner"],
                    "phone": info.get("phone", ""),
                    "entry_time": info["entry_time"].strftime('%Y-%m-%d %H:%M:%S')
                }
                for spot, info in self.parked_vehicles.items()
            },
            "history": self.history,
            "reserved_spots": list(self.reserved_spots)
        }
        
        with open("parking_data.json", "w") as f:
            json.dump(data, f, indent=4)
    
    def load_data(self):
        if os.path.exists("parking_data.json"):
            try:
                with open("parking_data.json", "r") as f:
                    data = json.load(f)
                
                # Load parked vehicles
                for spot_str, info in data.get("parked_vehicles", {}).items():
                    spot = int(spot_str)
                    self.parked_vehicles[spot] = {
                        "vehicle": info["vehicle"],
                        "type": info["type"],
                        "owner": info["owner"],
                        "phone": info.get("phone", ""),
                        "entry_time": datetime.strptime(info["entry_time"], '%Y-%m-%d %H:%M:%S')
                    }
                    self.parking_spots[spot] = info["vehicle"]
                
                # Load history
                self.history = data.get("history", [])
                
                # Load reserved spots
                self.reserved_spots = set(data.get("reserved_spots", []))
            except Exception as e:
                print(f"Error loading data: {e}")

def main():
    root = tk.Tk()
    app = ParkingManagementSystem(root)
    root.mainloop()

if __name__ == "__main__":
    main()