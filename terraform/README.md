# Deploying Couchbase with Terraform

1. Download an EC2 key pair to this directory.
2. Update `key_name` in `variables.tf` to make sure it matches the name of your key.
3. Run `terraform apply` and enter yes. The IP address of the Couchbase node(s) will be outputted to the console and saved in `ip_address.txt`.

After a couple of minutes, access the IP address in your browser with the :8091 port.

## Teardown

`terraform destroy`