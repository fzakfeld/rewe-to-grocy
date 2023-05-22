# REWE to Grocy

Sync your purchases at REWE to Grocy.

This Script will:
- Scrape all of your in-store purchases from REWE's Website (delivery not yet implemented)
- Sync the neccessary products to Grocy
- Add the purchased products as stock, including the price of purchase

The sync is still very simple and rudimentary, some features are not implemented yet. See this as a prototype ;)

## Usage

You'll need to specify the base path to your grocy installation, more specifically the API path. This usually looks something like this: `https://my-grocy-installation/api`

If you're using the Home Assistant Addon, you'll need to bind an external port to it in order to access Grocy without ingress, because that requires another layer of authentication.

In Grocy, there is a page where you can create an API key. You'll need to specify this as well in the configuration file.


The complicated part is getting an access token for the REWE website. Their API is not documented and not public, I just reversed engineered it. You need to login to https://shop.rewe.de and then get the cookie named 'rtsp', and copy the value in the configuration file.

As of now, this is the only way to use the REWE API (unofficially). You probably need to do this every time you run the script because the token is meant for the website and not long living. I am working on a better solution for this.

## License

See LICENSE.md for more information