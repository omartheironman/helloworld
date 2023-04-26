remote_state{
    backend = "gcs"
    disable_init = tobool(get_env("TG_DISABLE_INIT","false"))

    config = {
        bucket   = "helloworld-terraform-tg"
        prefix   = "${get_env("TF_VAR_region", "us-central1")}/${path_relative_to_include()}"
        project  = "${get_env("TF_VAR_project", "mythic-ego-384814")}"
        location = "us"
    }
}


terraform {
    extra_arguments "common_var"{
        commands = get_terraform_commands_that_need_vars()
        
    optional_var_files = [
        "${get_terragrunt_dir()}/default.tfvars",
        "${get_terragrunt_dir()}/${get_env("TF_VAR_region", "us-central1")}.tfvars",
        ]

    }
}