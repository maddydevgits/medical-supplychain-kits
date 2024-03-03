from flask import Flask,render_template,redirect,request,session

app=Flask(__name__)

@app.route('/')
def indexPage():
    return render_template('index.html')

if __name__=="__main__":
    app.run('0.0.0.0',port=5001,debug=True)