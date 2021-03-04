# Demystifying custom Machine Learning Algorithms with SageMaker


🚧📝 *Blog Post Project* - *WIP* 


If you’re in the game of productionizing Data Science algorithms, you must have certainly heard of SageMaker and what a powerful game-changing tool it is for Data Scientists.

There are two different levels to using SageMaker:

* [Built-in](https://docs.aws.amazon.com/sagemaker/latest/dg/algos.html) on-the-shelf models provided to you by SageMaker which are simple to use.
You don't have to have a deep understanding of what happens behind the scenes because SageMaker does most of the heavy lifting for you !
If you're looking to try one of the models on the list, it's quick and efficient.

* If you can't find what you're looking for on the shelf or face a hard limitation of a pre-built algorithm, you must get a deeper understanding of the way SageMaker works to do some heaving lifting of your own.
SageMaker remains an extremely powerful tool of this kind of use-cases!
It's not that hard to take your relationship with SageMaker to the next, it just requires a basic knowledge of skills, complementary to Machine Learning, such as Dockerization and APIs.

- Full costom mode : Follow up notebook `bring_your_own_example_1_sdk/notebooks/bring_your_own_gluonts_mlp.ipynb` to go through the functionnalities
- Built-in examples :  Follow [this](https://github.com/awslabs/amazon-sagemaker-examples/blob/master/sagemaker-python-sdk/1P_kmeans_highlevel/kmeans_mnist.ipynb) notebook example ( listed in this repo under `built_in_example_1_sdk` ), or other examples [here](https://github.com/awslabs/amazon-sagemaker-examples/tree/master/sagemaker-python-sdk)


## Appendix: Useful links
* Keep a close eye on:

| Topics  | 
| ---: | 
| [Ground Truth](https://aws.amazon.com/sagemaker/groundtruth/), [Active Learning](https://docs.aws.amazon.com/sagemaker/latest/dg/sms-automated-labeling.html) | 
| [PipeMode](https://docs.aws.amazon.com/sagemaker/latest/dg/cdf-training.html) | 
| Packing Large Dataset: [TFRecord](https://www.tensorflow.org/guide/data#consuming_tfrecord_data), RecordIO| 
| [Autopilot](https://docs.aws.amazon.com/sagemaker/latest/dg/autopilot-automate-model-development.html) | 
| [Anto scaling](https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling.html) | 
| [Inferentia](https://aws.amazon.com/machine-learning/inferentia/) | 
| [SageMaker Neo](https://aws.amazon.com/sagemaker/neo/) | 
| [SageMaker IDE](https://aws.amazon.com/fr/about-aws/whats-new/2019/12/introducing-amazon-sagemaker-studio-the-first-integrated-development-environment-ide-for-machine-learning/) | 

* Posts:
    * [Making the most out of your ML budget with SageMaker](https://medium.com/@julsimon/making-the-most-of-your-machine-learning-budget-on-amazon-sagemaker-a6982bdd5edd)
    * [SageMaker Bring Your Own](https://medium.com/smileinnovation/sagemaker-bring-your-own-algorithms-719dd539607d)
    * [Understanging SageMaker's Architecture](https://mlinproduction.com/sagemaker-architecture/)
    
* Github repos
    * [SageMaker Advanced Functionality](https://github.com/awslabs/amazon-sagemaker-examples/tree/master/advanced_functionality)
    * [SageMaker Python SDK Examples](https://github.com/awslabs/amazon-sagemaker-examples/tree/master/sagemaker-python-sdk)
