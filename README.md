# Simple Contact

Extremely simple contact form with a CAPTCHA. Entries are sent to the specified HTTP endpoint. 

JavaScript is not required to fill out the form, but if it is, then form fields are cached in localStorage.

## Building

1. Install `git`, `docker`, and `docker-compose`
2. 

```bash
git clone https://github.com/andrewkdinh/simple-contact.git
git clone https://github.com/daniel-e/rust-captcha.git
cd simple-contact
cp .env.example .env
# Edit .env
docker-compose up -d
```
3. Visit `http://localhost:8672`

## Credits

- Built with Python, Flask, Docker, Rust CAPTCHA, and water.css

Mirrors: [GitHub](https://github.com/andrewkdinh/simple-contact) (main), [Gitea](https://gitea.andrewkdinh.com/andrewkdinh/simple-contact)

Licensed under [AGPL 3.0](./LICENSE) | Copyright (c) 2021 Andrew Dinh
