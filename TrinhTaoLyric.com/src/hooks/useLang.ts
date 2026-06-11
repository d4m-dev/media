import { useCallback, useState } from "react";
import viVN from "../languages/vi-VN.json" assert { type: "json" };
import { languages } from "../languages/index.js";

export const useLang = (): [Language, (lang: string) => Promise<void>] => {
    const [value, setValue] = useState<Language>(viVN);

    const setLang = async (langCode: string): Promise<void> => {
        const l = await languages[`./${langCode}.json`]();
        setValue(l);
    };

    return [value, useCallback(async (lang: string) => setLang(lang), [])];
};
