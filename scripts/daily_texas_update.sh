#!/bin/bash
#
# Daily Texas Work Zone Update Script
# Runs the Texas work zone database update and logs the results
#
# Usage:
#   chmod +x scripts/daily_texas_update.sh
#   ./scripts/daily_texas_update.sh
#
# For cron:
#   0 2 * * * /path/to/Capstone/scripts/daily_texas_update.sh >> /path/to/Capstone/logs/texas_update.log 2>&1

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

# Log file with date
LOG_FILE="$PROJECT_DIR/logs/texas_update_$(date +%Y%m%d).log"

echo "================================================================" | tee -a "$LOG_FILE"
echo "Texas Work Zone Database Update" | tee -a "$LOG_FILE"
echo "Started: $(date)" | tee -a "$LOG_FILE"
echo "================================================================" | tee -a "$LOG_FILE"

# Change to project directory
cd "$PROJECT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..." | tee -a "$LOG_FILE"
    source venv/bin/activate
fi

# Run the update script
echo "Running update script..." | tee -a "$LOG_FILE"
python scripts/update_texas_database.py 2>&1 | tee -a "$LOG_FILE"

EXIT_CODE=$?

echo "" | tee -a "$LOG_FILE"
echo "================================================================" | tee -a "$LOG_FILE"
if [ $EXIT_CODE -eq 0 ]; then
    echo "✓ Update completed successfully" | tee -a "$LOG_FILE"
else
    echo "✗ Update failed with exit code $EXIT_CODE" | tee -a "$LOG_FILE"
fi
echo "Finished: $(date)" | tee -a "$LOG_FILE"
echo "================================================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

exit $EXIT_CODE
