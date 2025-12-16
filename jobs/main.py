import argparse, logging, sys
from config.job_config import JobConfig
from job_registry import JOB_REGISTRY


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MatchStream Spark Job Runner")
    parser.add_argument("--job", required=True, help="Job name (see job_registry.py)")
    return parser.parse_args()

def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

def main() -> None:
    setup_logging()
    logger = logging.getLogger(__name__)
    try:
        args = parse_args()
        if args.job not in JOB_REGISTRY:
            raise ValueError(f"Unknown job: {args.job}")
        config = JobConfig()
        job_entry = JOB_REGISTRY[args.job]
        logger.info(f"🚀 Starting job: {args.job}")
        
        # Handle both classes and factory functions
        if callable(job_entry) and not isinstance(job_entry, type):
            job = job_entry(config)
        else:
            job = job_entry(config=config)
            
        job.run()
        logger.info(f"✅ Finished job: {args.job}")
    except Exception as e:
        logger.error(f"Job failed: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()