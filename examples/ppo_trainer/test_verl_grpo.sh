export VLLM_ATTENTION_BACKEND=XFORMERS

export RAY_TMPDIR="/data/daiyp/ray"

MODEL_PATH="/nfs/turbo/coe-chaijy-unreplicated/pre-trained-weights/Qwen2.5-0.5B-Instruct"
DATA_PATH="/home/daiyp/OpenO1/deepscaler/parquet/gsm8k"

python3 -m verl.trainer.main_ppo \
 data.train_files=$DATA_PATH/train.parquet \
 data.val_files=$DATA_PATH/test.parquet \
 data.train_batch_size=1024 \
 data.val_batch_size=1312 \
 data.max_prompt_length=512 \
 data.max_response_length=256 \
 actor_rollout_ref.model.path=$MODEL_PATH \
 actor_rollout_ref.actor.optim.lr=1e-6 \
 actor_rollout_ref.actor.ppo_mini_batch_size=64 \
 actor_rollout_ref.actor.ppo_micro_batch_size=1 \
 actor_rollout_ref.rollout.log_prob_micro_batch_size_per_gpu=1 \
 actor_rollout_ref.rollout.tensor_model_parallel_size=1 \
 actor_rollout_ref.rollout.gpu_memory_utilization=0.4 \
 actor_rollout_ref.ref.log_prob_micro_batch_size_per_gpu=4 \
 critic.optim.lr=1e-5 \
 critic.model.path=$MODEL_PATH \
 critic.ppo_micro_batch_size=1 \
 algorithm.kl_ctrl.kl_coef=0.001 \
 +trainer.val_before_train=False \
 trainer.default_hdfs_dir=null \
 trainer.n_gpus_per_node=1 \
 trainer.nnodes=1 \
 trainer.save_freq=10 \
 trainer.test_freq=10 \
 trainer.total_epochs=15 \
 trainer.logger=\[console\]