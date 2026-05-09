import random

# Read both files
with open('/Users/workspace/pla_quiz_block.py', 'r') as f:
    quiz_block = f.read()

with open('/Users/workspace/ken_allen_app.py', 'r') as f:
    content = f.read()

# Split quiz block into two parts:
# Part 1 = QUIZ_DATA list (goes BEFORE the if/elif mode chain)
# Part 2 = elif quiz block (goes AFTER the last elif)
data_start = quiz_block.index('QUIZ_DATA = [')
elif_start = quiz_block.index('if mode == "🎯 Quiz":')
quiz_data_part = quiz_block[data_start:elif_start].strip()
quiz_elif_part = quiz_block[elif_start:].strip()

# Step 1: patch the mode radio to add Quiz tab
old_radio = '["🔍 Search", "📚 Browse", "📊 Insights & Network"]'
new_radio = '["🔍 Search", "📚 Browse", "📊 Insights & Network", "🎯 Quiz"]'

if old_radio in content:
    content = content.replace(old_radio, new_radio)
    print('Mode radio updated: ✅')
elif '🎯 Quiz' in content:
    print('Mode radio already updated: ✅')
else:
    print('WARNING: could not find radio line — check manually')

# Step 2: insert QUIZ_DATA before the if mode chain
insert_marker = 'if mode == "🔍 Search":'
if insert_marker in content:
    content = content.replace(
        insert_marker,
        quiz_data_part + '\n\n\n' + insert_marker
    )
    print('QUIZ_DATA inserted before mode chain: ✅')
else:
    print('WARNING: could not find if mode marker')

# Step 3: append the elif quiz block at the very end
content = content.rstrip() + '\n\n\n' + quiz_elif_part + '\n'
print('Quiz elif block appended: ✅')

# Step 4: write back
with open('/Users/workspace/ken_allen_app.py', 'w') as f:
    f.write(content)

print('ken_allen_app.py saved: ✅')
print('\nAll done! Now run:')
print('cd /Users/workspace && /Users/workspace/myenv/bin/streamlit run ken_allen_app.py')
