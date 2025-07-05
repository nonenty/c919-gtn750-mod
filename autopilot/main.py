# import matplotlib
# matplotlib.use('TkAgg')  # Set backend explicitly
# import matplotlib.pyplot as plt
# import numpy as np
from simconnect import SimConnect

class PIDController:
    def __init__(self, kp, ki, kd, lp=3, ld=3):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.lp = lp
        self.ld = ld
        self.prev_error = 0
        self.integral = 0
        self.derivative = 0
    
    def compute(self, setpoint, measurement, dt):
        error = setpoint - measurement
        self.integral += error * dt
        self.integral = max(-1, min(1,self.integral))
        self.derivative = (error - self.prev_error) / dt
        self.prev_error = error
        p = self.kp * max(-self.lp, min(self.lp, error))
        i = self.ki * self.integral
        d= self.kd * max(-self.ld, min(self.ld, self.derivative))
        return  p+i+d, p, i, d


"""Simple example of subscribing to a set of metrics"""

with SimConnect(name='MonitorMetrics2') as sc:
    simvars = [
        dict(name="AUTOPILOT FLIGHT DIRECTOR BANK", units="degree"),
        dict(name="AUTOPILOT FLIGHT DIRECTOR PITCH", units="degree"),
        dict(name="PLANE BANK DEGREES", units="degree"),
        dict(name="PLANE PITCH DEGREES", units="degree"),
        dict(name="L:C919X_CTRL_LEFT_SIDESTICK_ROLL", units="number"),
        dict(name="L:C919X_CTRL_LEFT_SIDESTICK_PITCH", units="number"),
        dict(name="AUTOPILOT MASTER", units="bool"),
    ]

    # but subscribe is more efficient if we're repeating...
    dd = sc.subscribe_simdata(simvars, period=0x02, interval=5)
    print(f"Subscribed to simvars with units {dd.get_units()}")

    # # Initialize plot windows
    # plt.ion()
    
    # # Pitch plot
    # fig_pitch, ax_pitch = plt.subplots(figsize=(10,6))
    # fig_pitch.canvas.manager.set_window_title('PID Controller - Pitch Tracking')
    # ax_pitch.set_title('PID Controller - Pitch Tracking')
    # ax_pitch.set_xlabel('Time (samples)')
    # ax_pitch.set_ylabel('Pitch (degrees)')
    # ax_pitch_pid = ax_pitch.twinx()  # Create secondary axis for PID terms
    # ax_pitch_pid.set_ylabel('PID Terms', rotation=270, va='bottom')
    # ax_pitch_pid.set_ylim([-1, 1])  # Fixed scale for PID terms
    
    # # Bank plot
    # fig_bank, ax_bank = plt.subplots(figsize=(10,6))
    # fig_bank.canvas.manager.set_window_title('PID Controller - Bank Tracking')
    # ax_bank.set_title('PID Controller - Bank Tracking')
    # ax_bank.set_xlabel('Time (samples)')
    # ax_bank.set_ylabel('Bank (degrees)')
    # ax_bank_pid = ax_bank.twinx()  # Create secondary axis for PID terms
    # ax_bank_pid.set_ylabel('PID Terms', rotation=270, va='bottom')
    # ax_bank_pid.set_ylim([-1, 1])  # Fixed scale for PID terms
    
    # plt.show(block=False)
    
    # Create data buffers for pitch and bank
    # max_points = 100
    # time_data = np.arange(max_points)
    
    # # Pitch data
    # pitch_desired = np.zeros(max_points)
    # pitch_current = np.zeros(max_points)
    # pitch_p = np.zeros(max_points)
    # pitch_i = np.zeros(max_points)
    # pitch_d = np.zeros(max_points)
    
    # # Bank data
    # bank_desired = np.zeros(max_points)
    # bank_current = np.zeros(max_points)
    # bank_p = np.zeros(max_points)
    # bank_i = np.zeros(max_points)
    # bank_d = np.zeros(max_points)
    
    # # Create pitch plot lines
    # line_pitch_desired, = ax_pitch.plot(time_data, pitch_desired, 'r-', label='Desired Pitch')
    # line_pitch_current, = ax_pitch.plot(time_data, pitch_current, 'b-', label='Current Pitch')
    # line_pitch_p, = ax_pitch_pid.plot(time_data, pitch_p, 'g--', label='P Term')
    # line_pitch_i, = ax_pitch_pid.plot(time_data, pitch_i, 'y--', label='I Term')
    # line_pitch_d, = ax_pitch_pid.plot(time_data, pitch_d, 'm--', label='D Term')
    # # Combine legends from both axes
    # lines_pitch, labels_pitch = ax_pitch.get_legend_handles_labels()
    # lines_pid, labels_pid = ax_pitch_pid.get_legend_handles_labels()
    # ax_pitch.legend(lines_pitch + lines_pid, labels_pitch + labels_pid)
    
    # # Create bank plot lines
    # line_bank_desired, = ax_bank.plot(time_data, bank_desired, 'r-', label='Desired Bank')
    # line_bank_current, = ax_bank.plot(time_data, bank_current, 'b-', label='Current Bank')
    # line_bank_p, = ax_bank_pid.plot(time_data, bank_p, 'g--', label='P Term')
    # line_bank_i, = ax_bank_pid.plot(time_data, bank_i, 'y--', label='I Term')
    # line_bank_d, = ax_bank_pid.plot(time_data, bank_d, 'm--', label='D Term')
    # # Combine legends from both axes
    # lines_bank, labels_bank = ax_bank.get_legend_handles_labels()
    # lines_pid, labels_pid = ax_bank_pid.get_legend_handles_labels()
    # ax_bank.legend(lines_bank + lines_pid, labels_bank + labels_pid)
    
    latest = 0
    pid_pitch = PIDController(kp=0.2, ki=0.0, kd=0.15, lp=3, ld=2)  # Pitch tuning
    pid_bank = PIDController(kp=0.3, ki=0.0, kd=0.06, lp=2, ld=5)  # Bank tuning
    last_time = None
    
    while True:
        while sc.receive(timeout_seconds=0.01):
            # clear queue of pending results, processed by receiver handlers
            # print('received result')
            pass
        n = len(dd.simdata.changedsince(latest))
        if n:
            # print(f"Updated {n} simvars")
            # print(dd.simdata)
            
            # Get current time and calculate delta time
            current_time = dd.simdata.latest()
            dt = (current_time - last_time) / 1000.0 if last_time else 0.1  # Convert to seconds
            last_time = current_time
            
            # Get current values
            desired_pitch = dd.simdata["AUTOPILOT FLIGHT DIRECTOR PITCH"]
            current_pitch = dd.simdata["PLANE PITCH DEGREES"]
            desired_bank = dd.simdata["AUTOPILOT FLIGHT DIRECTOR BANK"]
            current_bank = dd.simdata["PLANE BANK DEGREES"]
            
            # Compute pitch control
            pitch_output, pitch_p_term, pitch_i_term, pitch_d_term = pid_pitch.compute(
                desired_pitch, current_pitch, dt)
            pitch_output = -1 * max(-1.0, min(1.0, pitch_output))
            if dd.simdata["AUTOPILOT MASTER"] == 1.0:
                sc.set_simdatum(name="L:C919X_CTRL_LEFT_SIDESTICK_PITCH",
                            value=pitch_output, units="number")
            
            # Compute bank control
            bank_output, bank_p_term, bank_i_term, bank_d_term = pid_bank.compute(
                desired_bank, current_bank, dt)
            bank_output = -1 * max(-1.0, min(1.0, bank_output))
            if dd.simdata["AUTOPILOT MASTER"] == 1.0:
                sc.set_simdatum(name="L:C919X_CTRL_LEFT_SIDESTICK_ROLL",
                            value=bank_output, units="number")
            
            # # Update pitch plot data
            # pitch_desired = np.roll(pitch_desired, -1)
            # pitch_current = np.roll(pitch_current, -1)
            # pitch_p = np.roll(pitch_p, -1)
            # pitch_i = np.roll(pitch_i, -1)
            # pitch_d = np.roll(pitch_d, -1)
            
            # pitch_desired[-1] = desired_pitch
            # pitch_current[-1] = current_pitch
            # pitch_p[-1] = pitch_p_term
            # pitch_i[-1] = pitch_i_term
            # pitch_d[-1] = pitch_d_term
            
            # # Update bank plot data
            # bank_desired = np.roll(bank_desired, -1)
            # bank_current = np.roll(bank_current, -1)
            # bank_p = np.roll(bank_p, -1)
            # bank_i = np.roll(bank_i, -1)
            # bank_d = np.roll(bank_d, -1)
            
            # bank_desired[-1] = desired_bank
            # bank_current[-1] = current_bank
            # bank_p[-1] = bank_p_term
            # bank_i[-1] = bank_i_term
            # bank_d[-1] = bank_d_term
            
            # # Update pitch plot
            # line_pitch_desired.set_ydata(pitch_desired)
            # line_pitch_current.set_ydata(pitch_current)
            # line_pitch_p.set_ydata(pitch_p)
            # line_pitch_i.set_ydata(pitch_i)
            # line_pitch_d.set_ydata(pitch_d)
            # # Keep adaptive scaling for desired/current pitch
            # ax_pitch.set_ylim([
            #     min(np.min(pitch_desired), np.min(pitch_current))-1,
            #     max(np.max(pitch_desired), np.max(pitch_current))+1
            # ])
            
            # # Update bank plot
            # line_bank_desired.set_ydata(bank_desired)
            # line_bank_current.set_ydata(bank_current)
            # line_bank_p.set_ydata(bank_p)
            # line_bank_i.set_ydata(bank_i)
            # line_bank_d.set_ydata(bank_d)
            # # Keep adaptive scaling for desired/current bank
            # ax_bank.set_ylim([
            #     min(np.min(bank_desired), np.min(bank_current))-1,
            #     max(np.max(bank_desired), np.max(bank_current))+1
            # ])
            
            # # Update plot window
            # fig_pitch.canvas.draw_idle()
            # fig_bank.canvas.draw_idle()
            # plt.pause(0.01)  # Allow time for GUI events
            
            # # Check if windows were closed
            # if not plt.fignum_exists(fig_pitch.number) or not plt.fignum_exists(fig_bank.number):
            #     print("Plot window closed - exiting")
            #     break
            
            latest = current_time
