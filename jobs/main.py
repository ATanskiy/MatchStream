import argparse, logging
from job_registry import JOB_REGISTRY

def parse_args():
    parser = argparse.ArgumentParser(description="MatchStream Spark Job Runner")
    parser.add_argument("--job", required=True, help="Job name (see job_registry.py)")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.job not in JOB_REGISTRY:
        raise ValueError(f"Unknown job: {args.job}")

    JobClass = JOB_REGISTRY[args.job]

    logging.info(f"🚀 Starting job: {args.job}")
    job = JobClass()
    job.run()
    logging.info(f"✅ Finished job: {args.job}")

if __name__ == "__main__":
    main()