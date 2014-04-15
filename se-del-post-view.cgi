#!/usr/bin/perl
print "Content-type: text/html\n\n";

# this is where all my modules are
use FindBin;
use lib "$FindBin::Bin/../perllib";

# get the post ID the user requested
use CGI;
my $cgi = CGI->new();
my $id = $cgi->param('id');
if ($id !~ /^\d+$/) {
	print 'Invalid id - not a valid number';
	exit 1;
}

use WWW::Mechanize;

# log in
my $mech = WWW::Mechanize->new();
$mech->get('https://openid.stackexchange.com/account/login');
$mech->submit_form(with_fields => {
	email => 'INSERT EMAIL OF USER WITH 10K REP HERE',
	password => 'INSERT PASSWORD OF USER WITH 10K REP HERE'
});
$mech->get('http://stackoverflow.com/users/login');
$mech->submit_form(with_fields => {
	openid_identifier => 'https://openid.stackexchange.com/'
});

# find the deleted question the user requested
$mech->get("http://stackoverflow.com/q/$id");
$html = $mech->content();

# now let's parse it and get the data
use HTML::TreeBuilder::XPath;
my $xp = HTML::TreeBuilder::XPath->new();
$xp->parse_content($html);
# this is way overcomplicated. http://stackoverflow.com/a/9133579/
my @postData = $xp->findnodes('//*[contains(concat(" ", normalize-space(@class), " "), " question ")] | //*[contains(concat(" ", normalize-space(@class), " "), " answer ")]');
foreach my $post (@postData) {
	my $postText = $post->findnodes('.//div[@class="post-text"]')->get_node(1)->as_HTML();
	my $postVoteCount = $post->findnodes('.//span[contains(@class, "vote-count-post")]')->get_node(1)->as_text();
	print "$postVoteCount votes:<br>$postText<br><hr><br>";
}
