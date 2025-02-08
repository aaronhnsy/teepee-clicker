import javascript from "@eslint/js";
import next from "@next/eslint-plugin-next";
import jsxA11y from "eslint-plugin-jsx-a11y";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import typescript from "typescript-eslint";

export default typescript.config(
    {
        name: "eslint/ignores",
        ignores: [".next/"],
    },
    // javascript config
    {
        name: "javascript-eslint/all",
        ...javascript.configs.all,
    },
    {
        name: "javascript-eslint/overrides",
        rules: {
            "no-undef": "off",
            "no-alert": "off",
            "no-ternary": "off",
            "no-undefined": "off",
            "no-await-in-loop": "off",
            "no-magic-numbers": "off",
            "no-return-assign": "off",
            "no-nested-ternary": "off",
            "no-warning-comments": "off",
            "no-negated-condition": "off",
            "curly": "off",
            "one-var": "off",
            "new-cap": "off",
            "id-length": "off",
            "max-lines": "off",
            "sort-keys": "off",
            "func-style": "off",
            "max-params": "off",
            "sort-imports": "off",
            "max-statements": "off",
            "consistent-return": "off",
            "capitalized-comments": "off",
            "require-atomic-updates": "off",
            "max-lines-per-function": "off",
        },
    },
    // typescript config
    typescript.configs.strict,
    typescript.configs.stylistic,
    // typescript.configs.strictTypeChecked,
    // typescript.configs.stylisticTypeChecked,
    // {
    //     name: "typescript-eslint/type-checked",
    //     languageOptions: {
    //         parserOptions: {
    //             projectService: true,
    //             tsconfigRootDir: import.meta.dirname,
    //         },
    //     },
    // },
    {
        name: "typescript-eslint/overrides",
        rules: {
            "@typescript-eslint/no-unused-vars": "off",
        },
    },
    // react config
    {
        name: "react/strict",
        ...react.configs.flat.all,
        settings: { react: { version: "detect" } },
    },
    {
        name: "react/hooks",
        plugins: { "react-hooks": reactHooks },
        rules: reactHooks.configs.recommended.rules,
    },
    {
        name: "react/overrides",
        rules: {
            // jsx runtime
            "react/jsx-uses-react": "off",
            "react/react-in-jsx-scope": "off",
            // props
            "react/no-unused-prop-types": "off",
            "react/require-default-props": "off",
            "react/prefer-read-only-props": "off",
            "react/forbid-component-props": "off",
            "react/jsx-sort-props": "off",
            "react/jsx-indent-props": "off",
            "react/jsx-max-props-per-line": "off",
            "react/jsx-first-prop-new-line": "off",
            // misc
            "react/jsx-indent": "off",
            "react/jsx-newline": "off",
            "react/jsx-no-bind": "off",
            "react/no-multi-comp": "off",
            "react/jsx-max-depth": "off",
            "react/button-has-type": "off",
            "react/jsx-tag-spacing": "off",
            "react/jsx-no-literals": "off",
            "react/jsx-boolean-value": "off",
            "react/jsx-curly-newline": "off",
            "react/jsx-filename-extension": "off",
            "react/jsx-closing-tag-location": "off",
            "react/jsx-closing-bracket-location": "off",
        },
    },
    // next config
    {
        name: "next/strict",
        plugins: { "@next/next": next },
        rules: {
            ...next.configs.recommended.rules,
            ...next.configs["core-web-vitals"].rules,
        },
    },
    // jsx-a11y config
    jsxA11y.flatConfigs.strict,
    // tailwind config
    // tailwind.configs["flat/recommended"],
);