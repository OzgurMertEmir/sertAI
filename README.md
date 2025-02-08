# sertAI

## Raspberry Pi Setup
1. Update Package Lists
```bash
sudo apt-get update
```
2. Upgrade All Installed Packages (Optional but Recommended)
```bash
sudo apt-get upgrade
```
3. Install the PortAudio Dependencies
```bash
sudo apt-get install portaudio19-dev libportaudio2
```
4. Install pip (if not already installed)
```bash
sudo apt-get install python3-pip
```
Verify the installation by checking the pip version:
```bash
python3 -m pip --version
```
5. Clone the repository
```bash
git clone https://github.com/OzgurMertEmir/sertAI.git
```
6. Change the directory to the repository
```bash
cd sertAI
```
7. Create a virtual environment
```bash
python3 -m venv sert_venv
```
8. Activate the virtual environment
```bash
source sert_venv/bin/activate
```
9. Install the required packages
```bash
pip install -r requirements.txt
```
10. Create a .env file in the root directory of the repository
```bash
touch .env
```
11. Add the following environment variables to the .env file
- To edit the file
```bash
nano .env
```
- Add the following lines to the file
```bash
OPENAI_API_KEY="<YOUR_OPENAI_API_KEY>"
PORCUPINE_ACCESS_KEY="<YOUR_PORCUPINE_ACCESS_KEY>"
```
Then save the file and exit the editor.
12. Run a test script of your choice 
 - (Example for test_full_audio_pipeline_with_custom_wake_word_with_pi)
```bash
python3 -m unittest tests.audio_tests.MyTestCase.test_full_audio_pipeline_with_custom_wake_word_with_pi
```