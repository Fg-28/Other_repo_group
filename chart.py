from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import textwrap

app = Flask(__name__)

@app.route('/chart', methods=['POST'])
def chart():
    try:
        # ✅ Get data from POST request
        data = request.get_json()
        labels = data.get("labels", [])
        current = data.get("current", [])
        previous = data.get("previous", [])

        if not labels or not current or not previous:
            return jsonify({"error": "Missing data"}), 400

        # ✅ Wrap long labels to avoid overlap
        wrapped_labels = ['\n'.join(textwrap.wrap(label, 12)) for label in labels]

        # ✅ Bar positions and width
        x = np.arange(len(labels))
        width = 0.35

        # ✅ Setup chart
        bg_color = 'white'
        text_color = 'black'
        grid_color = 'gray'

        plt.figure(figsize=(10, 6), facecolor=bg_color)
        ax = plt.gca()
        ax.set_facecolor(bg_color)

        # ✅ Plot grouped bars
        bars1 = ax.bar(x - width/2, current, width, label='Current',
                       color='skyblue', edgecolor='white', linewidth=1)
        bars2 = ax.bar(x + width/2, previous, width, label='Previous',
                       color='orange', edgecolor='white', linewidth=1)

        # ✅ Add value labels on top of bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}',
                        ha='center', va='bottom', color=text_color, fontsize=9)

        # ✅ Axis labels and ticks
        ax.set_xlabel('LOB', color=text_color, fontsize=20, fontweight='bold')
        ax.set_ylabel('Quantity', color=text_color, fontsize=20, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(wrapped_labels, color=text_color, fontsize=12)
        ax.tick_params(colors=text_color)

        # ✅ Grid and legend
        ax.yaxis.grid(True, linestyle='--', color=grid_color, alpha=0.6)
        ax.xaxis.grid(False)
        ax.legend(facecolor=bg_color, edgecolor='gray', labelcolor=text_color)

        # ✅ Convert plot to base64 image
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

# ✅ Server settings (same as your original)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
