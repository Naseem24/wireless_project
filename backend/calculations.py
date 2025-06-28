# backend/calculations.py
import math

def calculate_wireless_system_logic(data):
    """Calculates rates at each block of a wireless comms system."""
    try:
        # Extract and convert input data, providing defaults
        bandwidth = float(data.get('bandwidth', 0))
        quantizer_bits = int(data.get('quantizerBits', 0))
        source_coder_rate = float(data.get('sourceCoderRate', 1)) # e.g., 0.25 for 4:1 compression
        channel_coder_rate = float(data.get('channelCoderRate', 1)) # e.g., 0.5 for rate-1/2 coding
        burst_size_bits = int(data.get('burstSizeBits', 0))

        # --- Calculations ---
        # Rate at Sampler Output (Nyquist Rate)
        sampler_rate_sps = 2 * bandwidth
        # Rate at Quantizer Output
        quantizer_rate_bps = sampler_rate_sps * quantizer_bits
        # Rate at Source Encoder Output (Compression)
        source_encoder_rate_bps = quantizer_rate_bps * source_coder_rate
        # Rate at Channel Encoder Output (Adds Redundancy)
        channel_encoder_rate_bps = source_encoder_rate_bps / channel_coder_rate if channel_coder_rate != 0 else 0
        # Interleaver does not change the rate
        interleaver_rate_bps = channel_encoder_rate_bps
        # Calculate burst duration based on the final rate
        burst_duration_s = burst_size_bits / channel_encoder_rate_bps if channel_encoder_rate_bps != 0 else 0

        # --- Structure the results with user-friendly keys and units ---
        return {
            "Sampler Rate": f"{sampler_rate_sps:,.0f} Sps",
            "Quantizer Rate": f"{quantizer_rate_bps:,.0f} bps",
            "Source Encoder Rate": f"{source_encoder_rate_bps:,.0f} bps",
            "Channel Encoder Rate": f"{channel_encoder_rate_bps:,.0f} bps",
            "Interleaver Output Rate": f"{interleaver_rate_bps:,.0f} bps",
            "Burst Duration": f"{burst_duration_s:.6f} s"
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        # Handle potential errors from bad input data
        return {"error": f"Invalid input or calculation error: {e}"}
    # Add this function to the end of backend/calculations.py

def calculate_ofdm_logic(data):
    """Calculates performance metrics for an OFDM system."""
    try:
        mod_order = int(data.get('modulationOrder', 0))
        rb_bw_khz = float(data.get('rbBw', 0))
        subcarrier_spacing_khz = float(data.get('subcarrierSpacing', 0))
        symbols_per_rb = int(data.get('symbolsPerRb', 0))
        parallel_rbs = int(data.get('parallelRbs', 0))
        rb_duration_ms = float(data.get('rbDurationMs', 0))

        # --- Calculations ---
        bits_per_symbol = math.log2(mod_order) if mod_order > 0 else 0
        subcarriers_per_rb = rb_bw_khz / subcarrier_spacing_khz if subcarrier_spacing_khz > 0 else 0
        bits_per_rb = bits_per_symbol * subcarriers_per_rb * symbols_per_rb
        
        rb_duration_s = rb_duration_ms / 1000
        max_data_rate_bps = (parallel_rbs * bits_per_rb) / rb_duration_s if rb_duration_s > 0 else 0
        
        total_bw_khz = parallel_rbs * rb_bw_khz
        spectral_efficiency = max_data_rate_bps / (total_bw_khz * 1000) if total_bw_khz > 0 else 0

        # --- Structure the results ---
        return {
            "Bits per Symbol": f"{bits_per_symbol:.2f}",
            "Subcarriers per RB": f"{subcarriers_per_rb:.2f}",
            "Bits per RB": f"{bits_per_rb:,.2f}",
            "Maximum Data Rate": f"{max_data_rate_bps / 1_000_000:.2f} Mbps",
            "Total Bandwidth": f"{total_bw_khz / 1000:.2f} MHz",
            "Spectral Efficiency": f"{spectral_efficiency:.2f} bps/Hz"
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        return {"error": f"Invalid input or calculation error: {e}"}
    # Add this function to the end of backend/calculations.py

def calculate_link_budget_logic(data):
    """Performs link budget calculations."""
    try:
        data_rate_bps = float(data.get('dataRateBps', 0))
        system_temp_k = float(data.get('systemTempK', 290))
        noise_figure_db = float(data.get('noiseFigureDb', 0))
        eb_no_db = float(data.get('ebNoDb', 0))
        fade_margin_db = float(data.get('fadeMarginDb', 0))
        path_loss_db = float(data.get('pathLossDb', 0))
        tx_gain_dbi = float(data.get('txGainDbi', 0))
        rx_gain_dbi = float(data.get('rxGainDbi', 0))
        other_losses_db = float(data.get('otherLossesDb', 0))
        
        BOLTZMANN_DBW_HZ_K = -228.6
        
        thermal_noise_dbw = BOLTZMANN_DBW_HZ_K + 10 * math.log10(system_temp_k) + 10 * math.log10(data_rate_bps) if system_temp_k > 0 and data_rate_bps > 0 else -999
        receiver_sensitivity_dbw = thermal_noise_dbw + noise_figure_db + eb_no_db
        required_rx_power_dbw = receiver_sensitivity_dbw + fade_margin_db
        required_tx_power_dbw = required_rx_power_dbw + path_loss_db + other_losses_db - tx_gain_dbi - rx_gain_dbi
        required_tx_power_watts = 10**(required_tx_power_dbw / 10)

        return {
            "Thermal Noise": f"{thermal_noise_dbw:.2f} dBW",
            "Receiver Sensitivity": f"{receiver_sensitivity_dbw:.2f} dBW",
            "Required Receiver Power": f"{required_rx_power_dbw + 30:.2f} dBm",
            "Required Transmitted Power": f"{required_tx_power_watts:.4f} W"
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        return {"error": f"Invalid input or calculation error: {e}"}
    # Add this function to the end of backend/calculations.py

def calculate_cellular_design_logic(data):
    """Performs cellular system design calculations."""
    try:
        total_area_sqkm = float(data.get('totalAreaSqkm', 0))
        cell_radius_km = float(data.get('cellRadiusKm', 0))
        num_subscribers = int(data.get('numSubscribers', 0))
        calls_per_hour = float(data.get('callsPerHour', 0))
        call_duration_min = float(data.get('callDurationMin', 0))
        blocking_prob = float(data.get('blockingProb', 0.02))
        sir_db = float(data.get('sirDb', 0))
        path_loss_exp = float(data.get('pathLossExp', 4))

        # --- Helper function for Erlang B ---
        def erlang_b(traffic, channels):
            if traffic < 0 or not isinstance(channels, int) or channels <= 0: return 1.0
            try:
                numerator = (traffic ** channels) / math.factorial(channels)
                denominator = sum([(traffic ** i) / math.factorial(i) for i in range(channels + 1)])
                return numerator / denominator if denominator > 0 else 1.0
            except (ValueError, OverflowError): # Handle large numbers
                return 1.0

        # --- Helper function to find channels ---
        def find_required_channels(traffic, target_prob):
            if traffic <= 0: return 0
            channels = 1
            while True:
                if erlang_b(traffic, channels) <= target_prob:
                    return channels
                channels += 1
                if channels > 1000: return -1 # Failsafe for unrealistic traffic

        # --- Main Calculations ---
        cell_area_sqkm = (3 * math.sqrt(3) / 2) * (cell_radius_km ** 2)
        num_cells = math.ceil(total_area_sqkm / cell_area_sqkm) if cell_area_sqkm > 0 else 0
        
        traffic_per_user_erlangs = (calls_per_hour * call_duration_min) / 60
        total_system_traffic_erlangs = num_subscribers * traffic_per_user_erlangs
        traffic_per_cell_erlangs = total_system_traffic_erlangs / num_cells if num_cells > 0 else 0

        channels_per_cell = find_required_channels(traffic_per_cell_erlangs, blocking_prob)
        
        sir_linear = 10**(sir_db / 10)
        cluster_size = math.ceil((1/3) * (6 * sir_linear)**(2 / path_loss_exp)) if path_loss_exp > 0 else 0

        return {
            "Number of Cells": f"{num_cells}",
            "Traffic per Cell": f"{traffic_per_cell_erlangs:.2f} Erlangs",
            "Channels per Cell (GoS)": "Not Found (High Traffic)" if channels_per_cell == -1 else f"{channels_per_cell}",
            "Required Cluster Size (N)": f"{cluster_size}"
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        return {"error": f"Invalid input or calculation error: {e}"}