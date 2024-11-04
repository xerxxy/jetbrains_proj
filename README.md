# jetbrains_proj

The project is organized like this: inside jetbrains_proj, I have all the files from the JetBrains project. There's a data folder that contains a raw directory with raw code files in different programming languages. Then I've got the processed directory, which has the data split into the format we need, and the tokenized directory, which holds the tokenized data used for running the code completion model.

I chose the big version of StarCoder because the dataset is pretty complex—it tries to capture the coding style of an entry-level programmer, and the code is a bit messy. I figured the tiny StarCoder wouldn't perform well enough.

In the root folder, we have run_dataset_split, run_dataset_tokenizer, and run_starcoder_inference. The first two just call modules inside src/data to tokenize and process the data.

The src directory inside jetbrains_project contains the main modules used to split the raw data and tokenize it. The way I split it is pretty straightforward—I tried to avoid cases where the middle section is invalid, like containing comments or empty lines. I also picked cases where the prefix is empty to create more generalized examples.

The Tokenize dataset just passes the data mentioned above through the tokenizer that's specifically chosen to match the model.

In src/constants, I store the constants I use so I don't have to hardcode values everywhere.

For metrics, besides exact match and chrF—which I'm not totally convinced about because they don't really consider the semantics of the code—I used others like Levenshtein distance, blind comparison, and the cosine similarity of the embeddings of the true middle and the predicted middle. In my view, this captures the semantics of the code better. It's kind of like how language models generate synonymous sentences. Another example is an autoencoder generating similar embeddings for similar images, word2vec... I also thought of using CodeBLEU for a more in-depth comparison.