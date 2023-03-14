const jsPsych = initJsPsych({
    extensions: [
        {type: jsPsychExtensionWebgazer}
    ]
});

var trials = [];

// Start screen
trials.push({
    type: jsPsychHtmlKeyboardResponse,
    stimulus: 'Hello world!'
});

// Initialize Camera
trials.push({
    type: jsPsychWebgazerInitCamera
});

// Calibrate Camera
trials.push({
    type: jsPsychWebgazerCalibrate,
    calibration_points: [[25,50], [50,50], [75,50], [50,25], [50,75]],
    calibration_mode: 'click'
});

// Validate Camera
trials.push({
    type: jsPsychWebgazerValidate,
    validation_points: [[-200,200], [200,200],[-200,-200],[200,-200]],
    validation_point_coordinates: 'center-offset-pixels',
    roi_radius: 100
});




jsPsych.run(trials);
