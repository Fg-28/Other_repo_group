from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

app = Flask(__name__)

@app.route('/chart', methods=['POST'])
def chart():
    try:
        data = request.get_json()
        labels = data.get("labels", [])
        current = data.get("current", [])
        previous = data.get("previous", [])

        if not labels or not current or not previous:
            return jsonify({"error": "Missing data"}), 400

        x = np.arange(len(labels))  # label positions
        width = 0.35  # width of each bar

        plt.figure(figsize=(10, 5), facecolor='black')
        ax = plt.gca()
        ax.set_facecolor('black')

        # ✅ Plot current and previous bars with borders
        bars1 = ax.bar(x - width/2, current, width, label='Current', color='skyblue', edgecolor='white', linewidth=1)
        bars2 = ax.bar(x + width/2, previous, width, label='Previous', color='orange', edgecolor='white', linewidth=1)

        # ✅ Add quantity labels above bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}',
                        ha='center', va='bottom', color='white', fontsize=9)

        ax.set_xlabel('LOB', color='white')
        ax.set_ylabel('Quantity', color='white')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, color='white')
        ax.tick_params(colors='white')

        # ✅ Add legend
        ax.legend(facecolor='black', edgecolor='white', labelcolor='white')

        # ✅ Save image
        buf = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buf, format="png", facecolor='black')
        buf.seek(0)
        encoded_image = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

        return jsonify({"image": f"data:image/png;base64,{encoded_image}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
