import os
import re
import uuid
import subprocess

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

app = FastAPI(title="Free Image to Video AI")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Hindi Piper voice model
PIPER_MODEL = os.path.join(
    BASE_DIR,
    "voices",
    "hi_IN-pratham-medium.onnx"
)


HTML = """
<!DOCTYPE html>
<html>
<head>

<title>Free Image to Video AI</title>

<style>

body {
    background:#0b0b0b;
    color:white;
    font-family:Arial,sans-serif;
    max-width:760px;
    margin:30px auto;
    padding:20px;
}

.box {
    background:#181818;
    padding:28px;
    border-radius:18px;
    box-shadow:0 0 30px #000;
}

h1 {
    text-align:center;
}

label {
    font-weight:bold;
    display:block;
    margin-top:12px;
}

input, select, textarea, button {
    width:100%;
    box-sizing:border-box;
    padding:13px;
    margin:8px 0 18px;
    border-radius:9px;
    border:none;
    font-size:16px;
}

textarea {
    height:130px;
    resize:vertical;
}

button {
    background:#2563eb;
    color:white;
    font-weight:bold;
    cursor:pointer;
}

button:hover {
    background:#1d4ed8;
}

#status {
    margin-top:20px;
    text-align:center;
    line-height:1.6;
}

video {
    width:100%;
    margin-top:25px;
    border-radius:12px;
}

.note {
    color:#aaa;
    font-size:13px;
    margin-top:-10px;
    margin-bottom:15px;
}

</style>

</head>

<body>

<h1>🎬 Free Image to Video AI</h1>

<div class="box">

<form id="form">

<label>Upload Image</label>

<input
    type="file"
    id="image"
    accept="image/*"
    required
>


<label>Prompt / Motion Description</label>

<textarea
    id="prompt"
    placeholder="Example: slow cinematic camera push-in, subtle movement, dark horror atmosphere..."
></textarea>


<label>Hindi Voice / Dialogue</label>

<textarea
    id="voice"
    placeholder='Optional. Example:
Neil: "कौन है?"
Rudra: "हमारे पीछे कौन खड़ा है?"
Ghost: "तुम्हारे पीछे... मैं हूँ!"

If left empty, quoted dialogues from the prompt will be used automatically.'
></textarea>

<div class="note">
💡 Put Hindi dialogues inside "..." or “...” for automatic voice generation.
</div>


<label>Duration</label>

<select id="duration">

<option value="30">
30 Seconds
</option>

<option value="60">
1 Minute
</option>

</select>


<label>Aspect Ratio</label>

<select id="ratio">

<option value="16:9">
16:9 Landscape
</option>

<option value="9:16">
9:16 Portrait
</option>

</select>


<button type="submit">
🎬 Generate Video + Hindi Audio — FREE
</button>

</form>


<div id="status"></div>

<video
    id="video"
    controls
    style="display:none"
></video>

</div>


<script>

const form =
    document.getElementById("form");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const image =
        document.getElementById("image").files[0];

    const prompt =
        document.getElementById("prompt").value;

    const voice =
        document.getElementById("voice").value;

    const duration =
        document.getElementById("duration").value;

    const ratio =
        document.getElementById("ratio").value;

    const status =
        document.getElementById("status");

    const video =
        document.getElementById("video");


    if (!image) {

        alert("Please select an image.");

        return;

    }


    status.innerHTML =
        "⏳ Processing...<br>" +
        "🎥 Creating cinematic animation...<br>" +
        "🎙️ Generating Hindi voice...<br>" +
        "🎬 Merging audio + video...";


    video.style.display = "none";


    const data =
        new FormData();

    data.append(
        "image",
        image
    );

    data.append(
        "prompt",
        prompt
    );

    data.append(
        "voice_text",
        voice
    );

    data.append(
        "duration",
        duration
    );

    data.append(
        "ratio",
        ratio
    );


    try {

        const response =
            await fetch(
                "/generate",
                {
                    method:"POST",
                    body:data
                }
            );


        if (!response.ok) {

            const text =
                await response.text();

            throw new Error(text);

        }


        const blob =
            await response.blob();


        const url =
            URL.createObjectURL(blob);


        video.src = url;

        video.style.display =
            "block";


        status.innerHTML =
            "✅ Video created successfully!<br>" +
            "🎙️ Hindi audio included.";


    }

    catch(error) {

        status.innerText =
            "❌ " + error.message;

    }

});

</script>

</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
async def home():

    return HTML


def extract_dialogue(prompt):

    """
    Extract text inside:
    "..."
    or
    “...”
    """

    matches = re.findall(
        r'"([^"]+)"|“([^”]+)”',
        prompt,
        flags=re.S
    )

    parts = []

    for normal, curly in matches:

        text = normal if normal else curly

        text = text.strip()

        if text:
            parts.append(text)

    return "\n".join(parts)


def run_command(command):

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(
            result.stderr[-3000:]
        )

    return result


@app.post("/generate")
async def generate(

    image: UploadFile = File(...),

    prompt: str = Form(
        "slow cinematic camera movement"
    ),

    voice_text: str = Form(""),

    duration: int = Form(30),

    ratio: str = Form("16:9")

):

    if duration not in [30, 60]:

        raise HTTPException(
            status_code=400,
            detail="Duration must be 30 or 60 seconds."
        )


    if ratio not in ["16:9", "9:16"]:

        raise HTTPException(
            status_code=400,
            detail="Invalid aspect ratio."
        )


    if not os.path.exists(PIPER_MODEL):

        raise HTTPException(
            status_code=500,
            detail=
            "Hindi Piper model not found: "
            + PIPER_MODEL
        )


    job_id = str(uuid.uuid4())


    input_file = os.path.join(
        TEMP_DIR,
        job_id + ".jpg"
    )


    silent_video = os.path.join(
        TEMP_DIR,
        job_id + "_silent.mp4"
    )


    voice_file = os.path.join(
        TEMP_DIR,
        job_id + "_voice.wav"
    )


    output_file = os.path.join(
        OUTPUT_DIR,
        job_id + ".mp4"
    )


    try:

        # ----------------------------
        # SAVE IMAGE
        # ----------------------------

        contents = await image.read()

        with open(
            input_file,
            "wb"
        ) as f:

            f.write(contents)


        # ----------------------------
        # VIDEO SIZE
        # ----------------------------

        if ratio == "16:9":

            width = 1280
            height = 720

        else:

            width = 720
            height = 1280


        # ----------------------------
        # CAMERA MOTION
        # ----------------------------

        prompt_lower = prompt.lower()


        # Default cinematic slow zoom

        if "zoom out" in prompt_lower:

            zoom_expression = (
                "if(lte(on,1),1.12,"
                "max(zoom-0.0008,1.0))"
            )

        else:

            zoom_expression = (
                "min(zoom+0.0008,1.12)"
            )


        # Horizontal movement

        if "move left" in prompt_lower:

            x_expression = (
                "iw/2-(iw/zoom/2)"
                "+(iw/zoom/5)"
            )

        elif "move right" in prompt_lower:

            x_expression = (
                "iw/2-(iw/zoom/2)"
                "-(iw/zoom/5)"
            )

        else:

            x_expression = (
                "iw/2-(iw/zoom/2)"
            )


        # Vertical movement

        if "move up" in prompt_lower:

            y_expression = (
                "ih/2-(ih/zoom/2)"
                "+(ih/zoom/8)"
            )

        elif "move down" in prompt_lower:

            y_expression = (
                "ih/2-(ih/zoom/2)"
                "-(ih/zoom/8)"
            )

        else:

            y_expression = (
                "ih/2-(ih/zoom/2)"
            )


        # ----------------------------
        # CINEMATIC VIDEO
        # ----------------------------

        filter_complex = (

            f"scale={width}:{height}:"
            "force_original_aspect_ratio=increase,"
            f"crop={width}:{height},"

            "zoompan="
            f"z='{zoom_expression}':"
            f"x='{x_expression}':"
            f"y='{y_expression}':"
            "d=1:"
            f"s={width}x{height}:"
            "fps=30,"

            "format=yuv420p"
        )


        video_command = [

            "ffmpeg",
            "-y",

            "-loop",
            "1",

            "-i",
            input_file,

            "-t",
            str(duration),

            "-vf",
            filter_complex,

            "-r",
            "30",

            "-c:v",
            "libx264",

            "-preset",
            "veryfast",

            "-crf",
            "22",

            "-pix_fmt",
            "yuv420p",

            silent_video

        ]


        run_command(video_command)


        # ----------------------------
        # VOICE TEXT
        # ----------------------------

        final_voice_text = (
            voice_text.strip()
        )


        # If voice field empty,
        # extract quoted dialogue
        # from prompt.

        if not final_voice_text:

            final_voice_text = (
                extract_dialogue(prompt)
            )


        # Fallback

        if not final_voice_text:

            final_voice_text = (
                "यह एक सिनेमैटिक दृश्य है। "
                "चारों तरफ सन्नाटा है। "
                "कैमरा धीरे धीरे आगे बढ़ता है।"
            )


        # ----------------------------
        # PIPER TTS
        # ----------------------------

        piper_command = [

            "python",
            "-m",
            "piper",

            "-m",
            PIPER_MODEL,

            "-f",
            voice_file,

            "--",

            final_voice_text

        ]


        run_command(piper_command)


        # ----------------------------
        # MERGE AUDIO + VIDEO
        # ----------------------------

        merge_command = [

            "ffmpeg",
            "-y",

            "-i",
            silent_video,

            "-i",
            voice_file,

            "-filter_complex",

            f"[1:a]"
            f"apad,"
            f"atrim=duration={duration}"
            f"[audio]",

            "-map",
            "0:v",

            "-map",
            "[audio]",

            "-t",
            str(duration),

            "-c:v",
            "copy",

            "-c:a",
            "aac",

            "-b:a",
            "128k",

            "-movflags",
            "+faststart",

            output_file

        ]


        run_command(merge_command)


        # ----------------------------
        # RETURN FINAL VIDEO
        # ----------------------------

        return FileResponse(

            output_file,

            media_type="video/mp4",

            filename="generated-video.mp4"

        )


    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


    finally:

        # Cleanup temporary files

        for file in [

            input_file,
            silent_video,
            voice_file

        ]:

            if os.path.exists(file):

                try:

                    os.remove(file)

                except:

                    pass