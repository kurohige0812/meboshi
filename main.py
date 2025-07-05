from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    rotation_result = []
    meboshi_result = []
    total_minutes = 0
    final_output = ""

    if request.method == "POST":
        rot_text = request.form.get("rotation_input", "")
        rotation_result = []
        for line in rot_text.strip().split("\n"):
            if "#" in line:
                parts = line.strip().split("#")
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    rotation_result.append((int(parts[0]), int(parts[1])))
        rotation_result.sort()

        mebo_text = request.form.get("meboshi_input", "")
        meboshi_result = []
        total_minutes = 0
        for line in mebo_text.strip().split("\n"):
            line = line.strip()
            if "円" in line or "玉" in line:
                parts = line.replace("円", " 円").replace("玉", " 玉").split()
                if len(parts) == 2 and parts[0].isdigit():
                    number = int(parts[0])
                    amount, unit = parts[1].split()
                    amount = int(amount)
                    if unit == "円":
                        minutes = round((amount / 500) * 2)
                    elif unit == "玉":
                        minutes = round((amount / 125) * 2)
                    else:
                        minutes = 0
                    total_minutes += minutes
                    meboshi_result.append((number, f"{amount}{unit}", minutes))
        meboshi_result.sort()

        lines = [f"{num}番台　{val}" for num, val in rotation_result]
        lines.append("\n――　目星　――\n")
        lines += [f"{num}番台　{amount}　{mins}分" for num, amount, mins in meboshi_result]
        lines.append(f"\n【合計 {total_minutes}分】")
        final_output = "\n".join(lines)

    return render_template("index.html",
                           rotation_result=rotation_result,
                           meboshi_result=meboshi_result,
                           total_minutes=total_minutes,
                           final_output=final_output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
