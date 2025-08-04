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

        x = np.arange(len(labels))
        width = 0.35

        # ✅ Use off-white background
        bg_color = '#f4f4f4'
        plt.figure(figsize=(10, 5), facecolor=bg_color)
        ax = plt.gca()
        ax.set_facecolor(bg_color)

        # ✅ Plot bars with white edge borders
        bars1 = ax.bar(x - width/2, current, width, label='Current',
                       color='skyblue', edgecolor='white', linewidth=1)
        bars2 = ax.bar(x + width/2, previous, width, label='Previous',
                       color='orange', edgecolor='white', linewidth=1)

        # ✅ Add labels above bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}',
                        ha='center', va='bottom', color='black', fontsize=9)

        # ✅ Add axis labels and ticks
        ax.set_xlabel('LOB', color='black')
        ax.set_ylabel('Quantity', color='black')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=45, color='black')
        ax.tick_params(colors='black')

        # ✅ Add horizontal gridlines
        ax.yaxis.grid(True, linestyle='--', color='gray', alpha=0.6)
        ax.xaxis.grid(False)

        # ✅ Legend with matching background
        ax.legend(facecolor=bg_color, edgecolor='gray', labelcolor='black')

        # ✅ Save image
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
