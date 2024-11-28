from flask import Flask,render_template,request,session


app = Flask(__name__)
app.secret_key = 'your_secret_key'

CUISINES = {
    "Indian Cuisine": ["Chole Bhature","Palak Paneer","Makke Di Roti and Sarson Da Saag","Hyderabadi Biryani","Vada Pav"],
    "Chinese Cuisine": ["Noodles"],
    "Italian Cuisine": ["Pollo alla Cacciatora","Melanzane alla Parmigiana","Lasagne alla Bolognese","Gnocchi di Patate","Fettuccine al Pomodoro"],
}

def new_recipes(file):
    recipes = []
    with open(file, "r") as f:
      
        
        current_recipe = {}
        current_section = None
    

        for line in f:
            line = line.strip()
            if line.startswith("Title:"):
                if current_recipe:
                    recipes.append(current_recipe)
                current_recipe = {"title": line.split("Title:")[1].strip(), "ingredients": [], "instructions": []}
            elif line.startswith("Ingredients:"):
                current_section = "ingredients"
            elif line.startswith("Instructions:"):
                current_section = "instructions"
            elif line and current_section == "ingredients":
                current_recipe["ingredients"].append(line)
            elif line and current_section == "instructions":
                current_recipe["instructions"].append(line)
        if current_recipe:
            recipes.append(current_recipe)
        
    return recipes

@app.route("/",methods=["GET"])
def index():
    selected_cuisine=request.args.get("cuisine")
    dishes=CUISINES.get(selected_cuisine,[]) if selected_cuisine else []
   
    return render_template("index.html", cuisines=CUISINES.keys(), selected_cuisine=selected_cuisine, dishes=dishes)
    

@app.route("/",methods=["GET","POST"])
def onclick():
   if request.method=="POST":
       print("Form data received:", request.form)
       selected_option=request.form.get("cuisine")
       selected_dish = request.form.get("dish")
       session["selected_option"] = selected_option
       session["selected_dish"] = selected_dish
       
       recipes = new_recipes(f"{selected_dish}.txt")
       
       
       

       print("Selected Option:",selected_option)
       return render_template("index2.html",recipes=recipes)
       
   





app.run(debug=True,port=8000)

