import {ProfileNetworthCalculator} from "skyhelper-networth";
import path from "path";
import fs from "fs";

const DATA_DIRECTORY = path.join(import.meta.dirname, "data");
const RESULT_DIRECTORY = path.join(import.meta.dirname, "result_node");

async function calculate(prices, user_data) {
    const calculator = new ProfileNetworthCalculator(
        user_data.profile,
        user_data.museum,
        user_data.balance,
    );
    return await calculator.getNetworth({prices: prices});
}

function main() {
    fs.mkdirSync(RESULT_DIRECTORY, {recursive: true});
    const prices = JSON.parse(fs.readFileSync(
        path.join(DATA_DIRECTORY, "prices.json"),
        "utf8",
    ));

    let promises = []
    for (const user_data of fs.readdirSync(DATA_DIRECTORY)) {
        if (user_data === "prices.json") continue;
        const data = JSON.parse(fs.readFileSync(
            path.join(DATA_DIRECTORY, user_data),
            "utf8",
        ));
        promises.push(calculate(prices, data).then(
            (networth) => {
                fs.writeFileSync(
                    path.join(RESULT_DIRECTORY, user_data),
                    JSON.stringify(networth),
                )
            }
        ));
    }
    Promise.allSettled(promises).then(() => process.exit(0))
}

main();
