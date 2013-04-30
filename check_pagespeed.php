#!/usr/bin/php
<?php
//include the class

class PageLoad {

        var $siteURL = "";
        var $pageInfo = "";

        /*
        * sets the URLs to check for loadtime into an array $siteURLs
        */
        function setURL($url) {
                if (!empty($url)) {
                        $this->siteURL = $url;
                        return true;
                }
                return false;
        }

        /*
        * extract the header information of the url
        */
        function doPageLoad() {
                $u = $this->siteURL;
                if(function_exists('curl_init') && !empty($u)) {
                        $ch = curl_init($u);
                        curl_setopt($ch, CURLOPT_HEADER, true);
                        curl_setopt($ch, CURLOPT_ENCODING, "gzip");
                        curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
                        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
                        curl_setopt($ch, CURLOPT_NOBODY, false);
                        curl_setopt($ch, CURLOPT_FRESH_CONNECT, false);

                        curl_setopt($ch, CURLOPT_USERAGENT, "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)");
                        $pageBody = curl_exec($ch);
                        $this->pageInfo = curl_getinfo($ch);
                        curl_close ($ch);

                        return true;
                }
                return false;
        }


        /*
        * compile the page load statistics only
        */
        function getPageLoadStats() {
                $info = $this->pageInfo;

                //stats from info
                $s['dest_url'] = $info['url'];
                $s['content_type'] = $info['content_type'];
                $s['http_code'] = $info['http_code'];
                $s['total_time'] = $info['total_time'];
                $s['size_download'] = $info['size_download'];
                $s['speed_download'] = $info['speed_download'];
                $s['redirect_count'] = $info['redirect_count'];
                $s['namelookup_time'] = $info['namelookup_time'];
                $s['connect_time'] = $info['connect_time'];
                $s['pretransfer_time'] = $info['pretransfer_time'];
                $s['starttransfer_time'] = $info['starttransfer_time'];

                return $s;
        }
}

// read in an argument - must make sure there's an argument to use
if ($argc==2) {

        //read in the arg.
        $url_argv = $argv[1];
        if (!eregi('^http://', $url_argv)) {
                $url_argv = "http://$url_argv";
        }
        // check that the arg is not empty
        if ($url_argv!="") {

                //initiate the results array
                $results = array();

                //initiate the class
                $lt = new PageLoad();

                //set the page to check the loadtime
                $lt->setURL($url_argv);

                //load the page
                if ($lt->doPageLoad()) {
                        //load the page stats into the results array
                        $results = $lt->getPageLoadStats();
                } else {
                        //do nothing
                        print "";
                }

                //print out the results
                if (is_array($results)) {
                        //expecting only one record as we only passed in 1 page.
                        $output = $results;
            if ($output['total_time'] >= 10.00000) {
                $checkstatus = 1;
                $exittext = "CRITICAL";
            }
            elseif ($output['total_time'] >= 7.0000) {
                $checkstatus = 2;
                $exittext = "WARNING";
            }
            else {
                $checkstatus = 0;
                $exittext = "OK";
            }

                    print "$exittext | ";
                        print "dns=".$output['namelookup_time']."s;;;0.000";
                        print " connect=".$output['connect_time']."s;;;0.00";
                        print " pretransfer=".$output['pretransfer_time']."s;;;0.00";
                        print " start=".$output['starttransfer_time']."s;;;0.00";
                        print " total=".$output['total_time']."s;7.00;10.00;0.00";
                        print " size=".$output['size_download']."B;;;0";
                        print " spd=".$output['speed_download'].";;;0.00\n";
            exit($checkstatus);
                } else {
                        //do nothing
                        exit(3);
                }
        }
} else {
        //do nothing
        exit(3);
}
?>
