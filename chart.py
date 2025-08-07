from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import base64
import textwrap

app = Flask(__name__)

@app.route('/chart', methods=['POST'])
def chart():
    try:
        data = request.get_json()
        labels = data.get("labels", [])
        values = data.get("values", [])

        if not labels or not values:
            return jsonify({"error": "Missing labels or values"}), 400

        # ✅ Wrap long labels to prevent overlap
        wrapped_labels = ['\n'.join(textwrap.wrap(label, 12)) for label in labels]

        # ✅ Set white background
        bg_color = 'white'
        text_color = 'black'
        grid_color = 'gray'

        plt.figure(figsize=(10, 6), facecolor=bg_color)
        ax = plt.gca()
        ax.set_facecolor(bg_color)

        # ✅ Plot bars
        bars = plt.bar(wrapped_labels, values, color='skyblue')

        # ✅ Add value labels above each bar
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height(), str(value),
                     ha='center', va='bottom', color=text_color, fontsize=10)

        # ✅ Grid and styling
        ax.yaxis.grid(True, linestyle='--', color=grid_color, alpha=0.6)
        ax.xaxis.grid(False)

        # ✅ Axis labels and ticks
        plt.xlabel("LOB", color=text_color, fontsize=20, fontweight='bold')
        plt.ylabel("Quantity", color=text_color, fontsize=20, fontweight='bold')
        plt.xticks(color=text_color, fontsize=12)
        plt.yticks(color=text_color, fontsize=10)

        # ✅ Save chart to base64-encoded image
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png", facecolor=bg_color)
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return jsonify({"image": f"data:image/png;base64,{encoded_image}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Keep original port and host settings
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
