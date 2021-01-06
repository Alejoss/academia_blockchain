const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');

module.exports = {
    entry: {
        certificate_preview: './src/certificate_preview/index.js',
    },
    mode: 'development',
    output: {
        path: path.resolve(__dirname, '../static/assets//bundles'),
        filename: '[name].bundle.js',
    },
    module: {
        rules: [
            {
                test: /\.s[ac]ss$/i,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
            },
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].bundle.css',
        }),
    ],
};
