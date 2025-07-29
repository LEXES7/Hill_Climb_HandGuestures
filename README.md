# 🏁 Hill Climb Racing Hand Gesture Controller

Control Hill Climb Racing using hand gestures detected through your webcam! No need for keyboard - just use your hands!

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.12.0-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.9-orange.svg)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey.svg)

## 🎮 Game Controls

| Gesture | Fingers | Action | Key |
|---------|---------|--------|-----|
| ✊ **Fist** | 0 fingers | Brake/Reverse | ⬅️ Left Arrow |
| ✋ **Open Hand** | 5 fingers | Accelerate | ➡️ Right Arrow |
| ☝️ **Point Up** | 1 finger | Lean Forward | ⬆️ Up Arrow |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam (built-in or external)
- macOS (optimized for Mac)
- Hill Climb Racing game

### Installation

1. **Clone the repository:**
   ```bash
   git clone 
   cd Hill_Climb_HandGuestures
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install opencv-python mediapipe pynput
   ```

### Usage

1. **Open Hill Climb Racing** on your computer
2. **Run the hand gesture controller:**
   ```bash
   python main.py
   ```
3. **Position your hand** in front of the camera
4. **Use gestures** to control the game:
   - Make a **fist** to brake
   - Show **open palm** to accelerate  
   - **Point up** to lean forward
5. **Press 'Q'** to quit

## 🛠️ Features

### ✅ Core Features
- **Real-time hand detection** using MediaPipe
- **Accurate finger counting** with 5-point landmark detection
- **Robust camera handling** with auto-reconnection
- **Visual feedback** with gesture indicators
- **Smooth control transitions** with action state management

### 🔧 Technical Features
- **Multi-camera support** - automatically tries different camera IDs
- **Error recovery** - handles camera disconnections gracefully
- **Performance monitoring** - frame rate tracking and health checks
- **Cross-platform compatibility** - optimized for macOS

## 📊 System Requirements

| Component | Requirement |
|-----------|-------------|
| **Python** | 3.8+ |
| **RAM** | 4GB minimum, 8GB recommended |
| **Camera** | Any USB webcam or built-in camera |
| **OS** | macOS 10.14+ (optimized) |
| **CPU** | Intel i5 or Apple M1+ |

## 🎯 How It Works

### Hand Detection Pipeline
1. **Camera Input** → Captures video stream
2. **MediaPipe Processing** → Detects hand landmarks (21 points)
3. **Finger Counting** → Analyzes fingertip positions vs base joints
4. **Gesture Recognition** → Maps finger count to game actions
5. **Keyboard Control** → Sends arrow key presses to game

### Finger Detection Logic
```python
# Fingertip landmark IDs
tipIds = [4, 8, 12, 16, 20]  # thumb, index, middle, ring, pinky

# Count extended fingers
for finger in fingers:
    if fingertip_y < joint_y:  # Finger is extended
        count += 1
```

## 🔧 Troubleshooting

### Camera Issues
- **Problem:** "Cannot read from camera"
- **Solution:** 
  1. Check camera permissions in System Preferences → Security & Privacy → Camera
  2. Close other apps using the camera (Zoom, Skype, etc.)
  3. Try different camera by changing `camera_id` in code

### Permission Issues  
- **Problem:** Keyboard control not working
- **Solution:**
  1. Grant accessibility permissions: System Preferences → Security & Privacy → Accessibility
  2. Add Terminal or your Python IDE to accessibility list

### Performance Issues
- **Problem:** Lag or slow detection
- **Solution:**
  1. Ensure good lighting
  2. Position hand 2-3 feet from camera
  3. Close unnecessary applications

## 📈 Performance Tips

### Optimal Setup
- **Lighting:** Bright, even lighting works best
- **Background:** Plain background improves detection
- **Distance:** 2-3 feet from camera for best accuracy
- **Hand Position:** Keep hand clearly visible and unobstructed

### Game Settings
- Set Hill Climb Racing to windowed mode for easier control
- Adjust game sensitivity if needed
- Ensure game window is in focus when using gestures

## 🔬 Technical Details

### Dependencies
```
opencv-python==4.12.0    # Computer vision and camera handling
mediapipe==0.10.9        # Hand landmark detection
pynput==1.8.1           # Keyboard control simulation
```

### Key Components
- **`initialize_camera()`** - Robust camera initialization with retry logic
- **Finger counting algorithm** - Geometric analysis of hand landmarks  
- **Action state management** - Prevents key press spam
- **Error recovery system** - Handles disconnections and failures

## 📸 Screenshots

### Gesture Recognition
```
✊ Fist (0 fingers) = BRAKE
[Red rectangle] "BRAKE" indicator

✋ Open Hand (5 fingers) = GAS  
[Green rectangle] "GAS" indicator

☝️ One Finger = LEAN FORWARD
[Blue rectangle] "LEAN FWD" indicator
```

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature-name`
3. **Commit** your changes: `git commit -m 'Add feature'`
4. **Push** to branch: `git push origin feature-name`
5. **Submit** a pull request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/yourusername/Hill_Climb_HandGuestures.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MediaPipe** team for excellent hand tracking
- **OpenCV** community for computer vision tools
- **Hill Climb Racing** for the awesome game
- **Python** community for amazing libraries

## 📞 Support

Having issues? Here's how to get help:

1. **Check** the troubleshooting section above
2. **Search** existing issues on GitHub
3. **Create** a new issue with:
   - Your OS version
   - Python version
   - Error messages
   - Steps to reproduce

## 🔄 Version History

- **v1.0.0** - Initial release with basic gesture control
- **v1.1.0** - Added camera reconnection and error handling
- **v1.2.0** - Improved finger detection accuracy
- **v1.3.0** - macOS optimization and performance improvements

## 🎮 Game Compatibility

Tested with:
- Hill Climb Racing (PC version)
- Hill Climb Racing 2 (PC version)
- Browser-based Hill Climb Racing games

## 🔮 Future Features

- [ ] Two-hand gesture support for more controls
- [ ] Gesture customization interface  
- [ ] Multiple game profiles
- [ ] Voice commands integration
- [ ] Mobile app companion

---

**Made with ❤️ for gamers who want to play hands-free!**

**⭐ Star this repo if you found it useful!**