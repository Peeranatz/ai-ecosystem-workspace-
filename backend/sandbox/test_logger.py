from utils.logger import logger, log_success, log_fail, log_execution

@log_execution(operation_name="Calculate Divide Operation")
def divide_numbers(a: float, b: float) -> float:
    return a / b

def run_logging_demo():
    print("=== 1. Testing Standard Log Levels ===")
    logger.debug("DEBUG: Diagnostic information for developers.")
    logger.info("INFO: General system lifecycle event.")
    logger.warning("WARNING: Potential issue or degraded performance detected.")
    logger.error("ERROR: Something went wrong, but application can continue.")

    print("\n=== 2. Testing SUCCESS Execution via Decorator ===")
    try:
        res = divide_numbers(10, 2)
        print(f"Result: {res}")
    except Exception:
        pass

    print("\n=== 3. Testing FAIL Execution via Exception Handling ===")
    try:
        res = divide_numbers(10, 0)
    except Exception as e:
        print(f"Caught expected error: {e}")

if __name__ == "__main__":
    run_logging_demo()
