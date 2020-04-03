from flask import Flask, render_template, request, redirect
import deezer_pl as deez
import create_podium as crp


def get_domain(url):
	try :
		res = url.split('.')[1]
	except :
		res = ""
	return res


app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/podium",methods=["POST"])
def podium():
	global infos
	link = request.form.get("link","")
	domain = get_domain(link)
	if domain=="deezer":
		infos = deez.recup_podium(link)
		crp.create(infos[2])
		return render_template("result.html")
	return redirect('/error')

@app.route("/error")
def error():
	return render_template("error.html")

@app.route("/ranking")
def rank():
    return render_template("rankings.html",tableau=infos[3].values.tolist())
    
if __name__ == "__main__":
    app.run(debug=True)



