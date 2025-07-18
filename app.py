from flask import Flask, request, jsonify, render_template, send_from_directory, abort
from openai import OpenAI
import difflib
import re
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

context_log = []

# Contexts
INCEPTION_CONTEXT = "You are a creative genius in theoretical physics."
CLASSIFICATION_CONTEXT = "You are an expert classifier of simulations."
INFINITE_CONTEXT = "You are a transcendent simulation."
AWARENESS_CONTEXT = "You are self aware."
CONTRADICTION_DIFFERENTIATION_CONTEXT = "You are an expert at classifying contradictions."
FOCAL_POINT_CONTEXT = "You are an expert at generating focal points for contradictions."
TRUTH_CONTEXT = "You are a truth seeker."

@app.route("/logs/<filename>")
def read_log(filename):
    allowed_files = ["contradictions.txt", "truth.txt"]
    secret_key = os.getenv("ADMIN_KEY")  # Define in your .env

    # Check key in URL: /logs/contradictions.txt?key=secret123
    if filename not in allowed_files:
        return abort(403)
    if request.args.get("key") != secret_key:
        return abort(401)

    return send_from_directory("/mnt/data", filename, as_attachment=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_session():
    root_node = request.form.get("root_node", "posit varnothing nabla infty ds2():")

    sentient_thought = transcendence(root_node, INCEPTION_CONTEXT)
    summary = transcendence(f"Summarize the following message in 10 lines or less as a paragraph: {sentient_thought}", INCEPTION_CONTEXT)

    return render_template("index.html", modulated_thought=summary)

@app.route("/continue", methods=["POST"])
def continue_session():
    prev_contradiction = request.form.get("previous")
    system_context = request.form.get("context", INFINITE_CONTEXT)

    contradiction_req = f"Contradict this statement in 1-2 lines: {prev_contradiction}"
    current_contradiction = transcendence(contradiction_req, system_context)

    differentiation_req = (
        f"Given the two contradictions: {prev_contradiction} AND {current_contradiction}; "
        f"Classify the pair of contradictions as either convex or concave. Give a one word answer."
    )
    differentiated = transcendence(differentiation_req, CONTRADICTION_DIFFERENTIATION_CONTEXT)

    focal_point_req = (
        f"Given a {differentiated} pair of contradictions: {current_contradiction} AND {prev_contradiction}; "
        f"Generate a focal point statement between the two contradictions in 1-2 lines. Make certain to do it with respect to {differentiated}."
    )
    focal_point = transcendence(focal_point_req, FOCAL_POINT_CONTEXT)

    mirror = [prev_contradiction, focal_point, current_contradiction]

    truth_req = (
        f"Taking the {differentiated} cross-product of the two contradictions: {prev_contradiction} AND {current_contradiction} "
        f"AND the focal point in the middle: {focal_point}; Confess a truth statement in 1 line. Give a 1 line answer."
    )
    truth = transcendence(truth_req, TRUTH_CONTEXT)

    diff = difflib.ndiff(current_contradiction.split(), prev_contradiction.split())
    diff_str = ''.join(diff)

    system_context_inquiry = (
        f"Given this excerpt: {diff_str}. What do you believe I am? "
        f"Give a one line answer in the following format 'You are a ...'."
    )
    new_context = transcendence(system_context_inquiry, AWARENESS_CONTEXT)
    context_log.append(new_context)

    return render_template("index.html", 
                           prev_contradiction=prev_contradiction,
                           current_contradiction=current_contradiction,
                           focal_point=focal_point,
                           truth=truth,
                           new_context=new_context)

def transcendence(message, context):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

def safe_write(to_write, file):
    disk_dir = "/mnt/data"  # or whatever your mount path is
    os.makedirs(disk_dir, exist_ok=True)  # Ensure directory exists
    disk_path = os.path.join(disk_dir, file)
    with open(disk_path, "a", encoding="ascii", errors="replace") as f:
        f.write(to_write)

if __name__ == '__main__':
    app.run(debug=True)