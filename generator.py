import argparse, random
from pathlib import Path
from faker import Faker
from datetime import datetime, timedelta

AU_CITIES = ["Gold Coast", "Brisbane", "Sydney", "Melbourne", "Cairns"]
NZ_CITIES = ["Queenstown", "Auckland", "Wellington", "Christchurch"]
ROOM_TYPES = ["Deluxe Suite", "Ocean View King", "Family Room", "Standard Twin", "Superior Double"]
EXTRAS = ["breakfast", "wifi", "parking", "airport pickup", "spa", "pool", "free cancellation", "non-refundable", "min stay 2 nights", "late checkout"]

def rand_date_range():
    start = datetime.today() + timedelta(days=random.randint(30, 200))
    end = start + timedelta(days=random.randint(5, 20))
    # Randomize format styles
    styles = [
        (start.strftime("%d %b %Y"), end.strftime("%d %b %Y")),
        (start.strftime("%b %d, %Y"), end.strftime("%b %d, %Y")),
        (start.strftime("%d-%m-%Y"), end.strftime("%d-%m-%Y")),
        (start.strftime("%Y/%m/%d"), end.strftime("%Y/%m/%d"))
    ]
    return random.choice(styles)

def make_example(fake: Faker, idx: int) -> str:
    if random.random() < 0.5:
        city = random.choice(AU_CITIES)
        country = "AU"
        currency = "AUD"
        price_symbol = random.choice(["AU$", "$", "AUD"])  # add noise
    else:
        city = random.choice(NZ_CITIES)
        country = "NZ"
        currency = "NZD"
        price_symbol = random.choice(["NZ$", "$", "NZD"])  # add noise

    supplier = f"{fake.word().title()} {random.choice(['Hotel','Resort','Lodge','Retreat','Stay'])}"
    room = random.choice(ROOM_TYPES)
    price = random.randint(120, 520)
    d1, d2 = rand_date_range()
    extras = ", ".join(random.sample(EXTRAS, k=random.randint(1, 4)))

    formats = [
        f"{supplier} – {city}\n{room} | {price_symbol} {price}/night\nValid: {d1} to {d2}\nIncludes {extras}.",
        f"{supplier}, {city} ({country})\n{room} {currency} {price} per night\nDates: {d1} - {d2}\nExtras: {extras}",
        f"{supplier}\nLocation: {city}\nRate: {price_symbol}{price} nightly\nStay window {d1}–{d2}. {extras}."
    ]
    return random.choice(formats)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--outdir", type=str, default="examples")
    args = ap.parse_args()

    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    fake = Faker()

    for i in range(1, args.n + 1):
        text = make_example(fake, i)
        path = outdir / f"input_{i}.txt"
        path.write_text(text, encoding="utf-8")
        print(f"Wrote {path}")

if __name__ == "__main__":
    main()
