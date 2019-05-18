// Imports the Google Cloud client library
import com.google.cloud.language.v1.Document;
import com.google.cloud.language.v1.Document.Type;
import com.google.cloud.language.v1.LanguageServiceClient;
import com.google.cloud.language.v1.Sentiment;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.DataSet;
import org.apache.flink.api.java.ExecutionEnvironment;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.api.java.utils.ParameterTool;
import org.apache.flink.util.Collector;

import java.io.IOException;

public class Analysis {

    public static void main(String[] args) throws Exception {

        final ParameterTool params = ParameterTool.fromArgs(args);

        // set up the execution environment
        final ExecutionEnvironment env = ExecutionEnvironment.getExecutionEnvironment();

        // make parameters available in the web interface
        env.getConfig().setGlobalJobParameters(params);

        // get input data
        DataSet<String> text;
        if (params.has("input")) {
            // read the text file from given input path
            text = env.readTextFile(params.get("input"));


            DataSet<Tuple2<String, Float>> counts =
                    // split up the lines in pairs (2-tuples) containing: (word,1)
                    text.flatMap(new Tokenizer());

            counts.sum(1).project(1).print();
            System.out.println("Contador"+counts.count());

            // emit result
            if (params.has("output")) {
                counts.writeAsCsv(params.get("output"), "\n", ",");
                // execute program
                env.execute("WordCount Example");
            } else {
                System.out.println("Printing result to stdout. Use --output to specify output path.");
                counts.print();
            }

        } else {
            // get default test text data
            System.out.println("Use --input to specify file input.");
        }


    }

    // *************************************************************************
    //     USER FUNCTIONS
    // *************************************************************************

    /**
     * Implements the string tokenizer that splits sentences into words as a user-defined
     * FlatMapFunction. The function takes a line (String) and splits it into
     * multiple pairs in the form of "(word,1)" ({@code Tuple2<String, Integer>}).
     */
    public static final class Tokenizer implements FlatMapFunction<String, Tuple2<String, Float>> {

        public void flatMap(String value, Collector<Tuple2<String, Float>> out) {
            // normalize and split the line
            
            // emit the pairs
            try (LanguageServiceClient language = LanguageServiceClient.create()) {


                // The text to analyze
                Document doc = Document.newBuilder()
                        .setContent(value).setType(Type.PLAIN_TEXT).build();

                // Detects the sentiment of the text
                Sentiment sentiment = language.analyzeSentiment(doc).getDocumentSentiment();

                //System.out.printf("Text: %s%n", value);
                //System.out.printf("Sentiment: %s, %s%n", sentiment.getScore(), sentiment.getMagnitude());

                out.collect(new Tuple2<>(value,sentiment.getScore()));
                
            } catch (IOException e) {
                System.out.println("oh no");
            }

        }
    }

        // Instantiates a client




}