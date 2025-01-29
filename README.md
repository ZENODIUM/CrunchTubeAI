# **CrunchTube AI** 🦈

CrunchTube AI is an innovative, AI-powered platform designed to revolutionize the way users interact with educational videos. By combining advanced technologies like YouTube video processing, Google Generative AI, and natural language processing, CrunchTube AI transforms lengthy lecture content into concise, actionable knowledge. Whether you're a student, educator, or lifelong learner, CrunchTube AI makes learning more efficient and engaging. 🚀

---

## **Key Features** ✨

### 1. **Video Analysis and Summarization** 📝
- Downloads YouTube videos and extracts subtitles (both manual and automatic).
- Uses AI to analyze video content and generate structured summaries with main topics, subtopics, and detailed explanations.
- Provides timestamped insights for quick navigation.

### 2. **Cheat Sheet Generation** 📄
- Creates beautifully formatted cheat sheets in PDF format summarizing the video content.
- Perfect for quick reference and revision.

### 3. **Text-to-Speech Conversion** 🗣🎧
- Converts the summarized content into audio using **Google Text-to-Speech (gTTS)**.
- Makes learning accessible for users who prefer listening over reading.

### 4. **YouTube Comments Sentiment Analysis** 📊
- Fetches and analyzes YouTube comments to provide insights into audience feedback.
- Summarizes comments to highlight key takeaways and potential caveats.

### 5. **Additional Study Materials** 🔗
- Generates a list of 10+ additional study materials with links related to the video topic.
- Helps users dive deeper into the subject matter.

### 6. **Visual Element Extraction** 🖼️
- Extracts specific frames from videos based on timestamps.
- Crops visual elements (e.g., diagrams or slides) for better understanding.

---

## **How It Works** ⚙️

1. **Input**: Users provide a YouTube video link through the web interface.
2. **Processing**:
   - The app downloads the video and subtitles using `yt-dlp`.
   - Subtitles are analyzed by Google Generative AI to extract topics, subtopics, and content.
   - Visual elements are identified and cropped based on timestamps.
3. **Output**:
   - Summaries, cheat sheets (PDF), audio files (MP3), and additional resources are generated.
   - Insights from YouTube comments are analyzed and presented.

---

## **Technologies Used** 💻

- **Flask**: Backend framework for building the web application.
- **yt-dlp**: For downloading YouTube videos and subtitles.
- **OpenCV**: Extract parts of the video.
- **Google Generative AI (Gemini Models)**: For analyzing video content, generating summaries, cheat sheets, and additional materials.
- **gTTS (Google Text-to-Speech)**: For converting text summaries into audio files.
- **Google API (YouTube Data API)**: For fetching video metadata and comments.
- **Mermaid Js**: For generating Flowchart.
- **Chart Js**: For creating the difficulty vs timestamp chart.

---

## **Benefits of CrunchTube AI** 🌟

1. Saves time by condensing hours of video content into concise summaries.
2. Enhances learning with cheat sheets, audio summaries, and additional resources.
3. Improves accessibility for visually impaired users or those who prefer auditory learning.
4. Provides insights into audience feedback through YouTube comment analysis.
5. Empowers students and educators to focus on learning rather than note-taking.

---

## **Ideal Use Cases** 🎯

- Students preparing for exams or revising lectures quickly.
- Educators creating supplementary materials for their classes.
- Lifelong learners looking to grasp complex topics efficiently.
- Content creators analyzing audience feedback on their videos.

---

## **Future Enhancements** 🔮

1. Multilingual support for subtitles and summaries 🌍.
2. Integration with more video platforms like Vimeo or Dailymotion 📺.
3. Advanced analytics for deeper insights into video content 📊.
4. Real-time processing for live lectures or webinars ⏱️.

---

CrunchTube AI is your ultimate companion for smarter, faster, and more effective learning! 📚
